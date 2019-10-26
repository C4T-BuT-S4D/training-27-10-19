module Rushmallow.Cryptography.Primitives.Polynomial

open Rushmallow.Cryptography.Common


let PolynomialEval (coefficients: bigint list) (x: bigint) : bigint =
    coefficients
    |> Seq.rev
    |> Seq.zip (seq { 0 .. coefficients.Length } |> Seq.map bigint)
    |> Seq.map (fun (power, coefficient) -> bigint.ModPow(x, power, Modulus) * coefficient)
    |> Seq.fold (+) (bigint 0)
    |> (%) <| Modulus
