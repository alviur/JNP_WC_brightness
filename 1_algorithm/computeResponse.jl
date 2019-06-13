import ImageMagick
using ImageMagick
import Pkg; Pkg.add("Images")
import Pkg; Pkg.add("Plots")
Pkg.add("ImageMagick")
import Pkg; Pkg.add("FFTW")
Pkg.add("JLD")
using JLD
using Images


import Pkg
#Pkg.add("ContrastEnhancement")
include("./ContrastEnhancement.jl")
#Pkg.activate("ContrastEnhancement")

using Main.ContrastEnhancement
import Plots


% Paths
path = "/home/alexander/Desktop/JNP_italians/2_data/Illusions/white"
savePath = "/home/alexander/Desktop/JNP_italians/3_Results/whiteWC_cortical/"