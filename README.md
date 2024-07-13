# arrowey   
An easy, 2D esolang made from an almost-unreadable programming language, both implemented in this repo.   
> [!WARNING]   
> *Do not clone the repo to try to run arrowey in a production environment, the code **will** have problems and 
> **will** crash sometimes because it is between versions!*   
> If you wish to run arrowey, check out the releases page.   

There isn't really a "spec", there's only this implementation of arrowey, the spec is in my head. 
I'll write documentation later on, at first I want to get it into working shape 
(i.e. at least most syntax implemented in the parser and first run of a basic I/O and arithmetics program).   

   
*NOTE: I'm very irregularly working on this project as I don't always have time for it because of school...*   
   
   
# Notes about arrowey itself
* arrowey is a strongly-typed language, meaning that you have to explicitly convert variables to a different type to use 
them as that different type, ints and floats are the only exceptions from that rule and can e.g. directly be inserted 
and used together in arithmetic operations without explicit conversion, in that case the operation always returns a 
float.
* If given, variable type assignments are strictly enforced. Untyped variables are technically typed `any` and can thus 
hold any type. Here, no exception for ints and floats is made, so you cannot assign an integer or float to a string-only
typed variable. You also can't assign a float to an int variable or vice versa, so keep that in mind when trying to do 
arithmetic with mixed numbers.   
Integers can be bit-limited by assigning them a whole number in the type assignment, e.g. `(int(8))<x> = 255` to 
create the 8-bit-integer variable `<x>` with the value 255. You cannot assign a list of numbers to a single type, but 
you can assign a list of types with different lengths. In type casting the same is true.   
Vectors can be fixed to a specific amount of dimensions (e.g. `(vec(3))<dims> = (<x>|<y>|<z>)` for a 3D vector) by 
assigning them a whole number in the type assignment. You cannot assign a list of numbers for vector dimensions, but you
can assign a list of types with different dimension counts. Casting a vector to a different vector either removes 
dimensions from the end of the vector's dimension list or adds zeroed ones, depending on if dimensions are removed or 
added. A type assignment of `vec(1)` is functionally identical to a type assignment of  `float`. 
* Vectors can either be float vectors (`vec`) or int-only vectors (`intvec`). One-dimensional vectors don't exist and 
casting to a one-dimensional vector converts the given number / given vector's first dimension to float for `vec` or to 
int for `intvec`. Zero-dimensional vectors are automatically interpreted as `<>` and negative-dimension vectors are 
interpreted as the same positive-dimension vector (e.g. `vec(-3)` is identical to `vec(3)`).
* 