mswine
=======

Multivariative Simplicial Weight Interpolation / Extrapolation.

This project is an implementation of four different interpolation and extrapolation technics with a few demos and utilities.

![Screenshot](/assets/screenshot.png "Screenshot")

F_w - is the average weighted interpolation, also called baricentric. It is a global scheme.

F_b - is the baricentric weighted simplicial interpolation. It is local and does not provide derivative continuousness. Neigher it has an extrapolation method implemented.

F_l - is the linear simplicial weighted interpolation. It is a local scheme, so it needs simplicial complex, given as a list of simplexes, to operate. Note that while interpolation function itself is continuous, its derivatives are generaly not.

F_s - simplicial weighted interpolation. It is local, and being used with appropriate weighting function and basis functions, can provide derivative continuousness up to any choosen level.

Extrapolation provided for every scheme.

![Extrapolation](/assets/figure_1.png "Extrapolation")

Some of the code is being ported to C# in my new project "Unpager": https://github.com/akalenuk/unpager

There is one academic <a href="docs/simpl_nie_engl.docx">article</a> on the topic translated in English and a couple in Ukrainian in the /docs folder.

The code itself is poorly documented and there is little matherial on the topic, so feel free to ask anything by email: akalenuk@gmail.com 
