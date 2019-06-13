"""
Computes the gradient of an image with periodic boundary condition.

We prefer to use the imgradients function in the Images package.

Returns:
- `gradx`
- `grady`
"""
function gradient(F::Array{T,2}; h = 1.) where T<: Number

	# fix the column-wise storing of the image
	# F = F'

	s = size(F)
	gradx = similar(F)
	grady = similar(F)

  gradx = (circshift(F,[-1,0]) - circshift(F,[1,0]))/2/h
  grady = (circshift(F,[0,-1]) - circshift(F,[0,1]))/2/h

	return gradx, grady
end

"""
Lift an image N1xN2 to the V1 representation of dimension N1xN2xθs, using
the gradient.

Arguments:

- `grad_type` = type of gradient to use
"""
function lift_petitot(img, θs::Integer; epsGrad = 1e-4, bottomLevel = 1e-4, grad_type = :difference, args...)

	if grad_type == :difference
		gradx, grady = gradient(img)
	elseif grad_type == :filter
		grady, gradx = imgradients(img)
	elseif grad_type == :fourier
		f_img = img |> fft |> fftshift
		cent = (size(img,1)+1)/2
		f_gradx =  Complex{Float64}[ (λ-cent)*f_img[λ, μ] for λ = 1:size(img,1), μ=1:size(img,2)]
		f_grady =  Complex{Float64}[ (μ-cent)*f_img[λ, μ] for λ = 1:size(img,1), μ=1:size(img,2)]
		gradx = f_gradx |> ifftshift |> ifft |> imag
		grady = f_grady |> ifftshift |> ifft |> imag
	end

	gradNorm = sqrt.(abs.(gradx).^2+abs.(grady).^2)

	# Generate the matrix of directions
	dirMatrix = similar(img, Int64)
	for i=1:size(img, 1), j=1:size(img, 2)
		if gradNorm[i,j] > epsGrad
			dirMatrix[i,j] = mod1(round(Int, (atan(grady[i,j], gradx[i,j]) + pi/2)* θs/pi), θs)
		else
			dirMatrix[i,j] = -1
		end
	end

	imgLift = zeros((size(img, 1),size(img, 2),θs))
	for i=1:size(img, 1), j in 1:size(img, 2)
		if dirMatrix[i,j] != -1
			imgLift[i,j,dirMatrix[i,j]] = img[i,j]
		else
			imgLift[i,j,:] = (img[i,j] / θs)*ones(θs)
		end
	end

	return imgLift
end

fft_lift(lift) = fftshift(fft(lift, [1,2]), [1,2])
ifft_lift(flift) = real( ifft( ifftshift(flift, [1,2]), [1,2]) )