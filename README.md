<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Modulus Wave Equation" />

  &#xa0;

  <!-- <a href="https://moduluswaveequation.netlify.app">Demo</a> -->
</div>

<h1 align="center">Modulus Wave Equation</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/JustinLinKK/modulus-wave-equation?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/JustinLinKK/modulus-wave-equation?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/JustinLinKK/modulus-wave-equation?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/JustinLinKK/modulus-wave-equation?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/JustinLinKK/modulus-wave-equation?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/JustinLinKK/modulus-wave-equation?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/JustinLinKK/modulus-wave-equation?color=56BEB8" /> -->
</p>

<!-- Status -->

<h4 align="center"> 
	🚧  Modulus Wave Equation 🚀 Under construction...  🚧
</h4> 

<hr>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#construction-ToDo">ToDo</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="#memo-Citation">Citation</a> &#xa0; | &#xa0;
  <a href="https://github.com/JustinLinKK" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

This is the example for wave equations from 1 dimension to 3 dimensions. It is froked from the [Mudulus-Sym-examples](https://docs.nvidia.com/deeplearning/modulus/modulus-sym/user_guide/foundational/1d_wave_equation.html) with additional code attached so you can create your own dataset using the additional code and [Devito](https://www.devitoproject.org/) library.

## :sparkles: Features ##

:heavy_check_mark: Use the Neural Network and [CUDA Toolkits](https://docs.nvidia.com/cuda/doc/index.html) to solve the wave equation;\
:heavy_check_mark: Same precision as the Benchmark result from [Devito](https://www.devitoproject.org/) and less error caused by the boundary reflection;\
:heavy_check_mark: Added the 3D wave equation example;

## :construction: ToDo ##

- Find the proper Plotter for the 3D example in vaildation;
- Update all the comment in the code line;
- Find the proper way to post process the result in ParaView;


## :rocket: Technologies ##

The following tools were used in this project:

- [Mudulus-Sym](https://docs.nvidia.com/deeplearning/modulus/modulus-sym/user_guide/getting_started/installation.html)
- [Devito](https://www.devitoproject.org/)
- [Pytorch](https://pytorch.org/)
- [ParaView](https://www.paraview.org/)
- [OpenFoam](https://www.openfoam.com/)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Devito](https://www.devitoproject.org/), [ParaView](https://www.paraview.org/) and [Modulus-Sym](https://docs.nvidia.com/deeplearning/modulus/modulus-sym/user_guide/getting_started/installation.html) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/JustinLinKK/modulus-wave-equation

# Access
$ cd modulus-wave-equation

# Install dependencies
$ pip install -r requirements.txt

# Run the project based on the example you want
```

## :memo: License ##

This project is under license from GPL-3.0. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/JustinLinKK" target="_blank">JustinLinKK</a>

&#xa0;



## :memo: Code Citation ##
[Modulus-Sym](https://github.com/NVIDIA/modulus-sym)

<a href="#top">Back to top</a>