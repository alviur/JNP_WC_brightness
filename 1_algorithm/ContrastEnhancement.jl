module ContrastEnhancement

import ImageMagick
using ImageMagick
using Images
using FFTW

include("cakes.jl")
include("petitot_lift.jl")

export wc, lhe

# Lift code:

function lift(img, θs; lift_type = :cakes, args...)
    @assert lift_type == :cakes || lift_type == :petitot
    if lift_type == :cakes
        return lift_cake(img, θs; args...)
    elseif lift_type == :petitot
        return lift_petitot(img, θs; args...)
    end
end

normalize(x) = typeof(x)(x - ones(size(x))*minimum(x))/(maximum(x)-minimum(x))

function project(Lf; normalized = true, args...) 
    x = sum(Lf, dims = 3)[:,:,1]
    normalized ? x = normalize(x) : nothing
    return Gray.(x)
end

# Approximation sigmoid for LHE

# Coefficients of the polynomial approximation of the sigmoid
const c = reverse([-7.7456e+00, 
                3.1255e-16, 
                1.5836e+01, 
                -1.8371e-15, 
                -1.1013e+01, 
                4.4531e-16, 
                3.7891e+00, 
                1.2391e-15]);

#Degree of the approximating polynomial
const n = length(c)-1;  

gr(i,img,ω) = imfilter(img.^i,ω)
a(i,img)=sum( [(-1.)^(j-i+1)*c[j+1]*binomial(j,i)*Float64.(img).^(j-i) for j in i:n] )
R(img,ω) = sum( [ a(i,img) .* gr(i,img,ω) for i in 0:n ] )

# Weight functions generation
function adapted_gaussian(σ::Number, I; args...)
    # Generates a Gaussian with variance σ and correct
    # dimensions w.r.t. to I

    if ndims(I) == 2
        var = (σ, σ)
    else
        var = (σ, σ, (size(I, 3)/size(I, 1))*σ)
    end

    # var = tuple([σ for _ in 1:ndims(I)]...)
    Kernel.gaussian(var) |> reflect # Convolution not correlation
end

# Local Mean Average, to be used as M in the numerical scheme
# if σμ is a tuple, it generates a Sum of Gaussians, as in the
# espada code
LMA(σμ, I0; args...) = imfilter(I0, adapted_gaussian(σμ, I0))

function gradient_descent(I0, W, λ, lma; Δt = .15, threshold = .01, max_iter = 50, M=1, args...)
	# σμ: std deviation for the local mean average
    # σw: std deviation for the contrast kernel w
    # lma: local mean average of the starting image
    # threshold : the iterations stops when two successive terms have a weighted L2 difference smaller than this quantity
    # max_iter: maximum number of iterations
    
#     println(typeof(W))
#     display(Gray.(W(I0)))
    next(Ik) = (1-(1+λ)Δt)Ik + (lma + W(Ik)/(2*M))Δt + λ*Δt*I0
    proj(x) = sum(x, dims = 3) # it does nothing if x has 2 dims
    diff(a,b) = sqrt( sum(( proj(a-b) ).^2)/sum(proj(a).^2) )

    prec = I0
    cur = next(I0)
    i = 1
    while diff(prec, cur) >= threshold && i < max_iter
        (prec, cur) = (cur, next(cur))
        i += 1
    end

    (cur, i, diff(prec, cur))
end

function algo(I0, σμ, σw, λ; algo_type = :planar, model = :wc, θs = 30, α = 5, args...) 
    
	if algo_type == :cortical
		F0 = lift(Float64.(I0), θs; args...)
		lma = lift(Float64.(LMA(σμ, I0)), θs; args...)
	elseif algo_type == :planar
		F0 = copy(I0)
		lma = LMA(σμ, I0)
	else
		error("Type of evolution must be :cortical or :planar")
	end

	if model == :wc
		σ(x) = min(max(α*x, -1),1)
		W(I) = imfilter(σ.(I),adapted_gaussian(σw, F0))
		
		# below we put the contribution of the 
		# local mean to 0 (it seems more 
		# reasonable for wc)
        res = gradient_descent(F0, W, λ, 0*lma; args...)
	elseif model == :lhe
		W2(I) = R(I, adapted_gaussian(σw, F0))
        res = gradient_descent(F0, W2, λ, lma; args...)
    else
		error("Model must be :wc or :lhe")
	end


	if algo_type == :cortical
		return (project(res[1]; args...), res[2:end])
	elseif algo_type == :planar
		return res
	end	
end

wc(I0, σμ, σw, λ; args...) = algo(I0, σμ, σw, λ, model = :wc; args...) 
lhe(I0, σμ, σw, λ; args...) = algo(I0, σμ, σw, λ, model = :lhe; args...)

end