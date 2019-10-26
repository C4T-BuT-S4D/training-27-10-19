module Rushmallow.Cryptography.SSS

open Rushmallow.Cryptography.Primitives.RandomGenerator
open Rushmallow.Cryptography.Primitives.StringConverter
open Rushmallow.Cryptography.Primitives.Polynomial
open Rushmallow.Cryptography.Common


let ExposeSecret (secret: string) : bigint list = 
    seq { 1 .. 8 } 
    |> Seq.map (bigint >> (PolynomialEval <| GenerateManyNumbers Size @ [secret |> MakeInteger]))
    |> Seq.toList
