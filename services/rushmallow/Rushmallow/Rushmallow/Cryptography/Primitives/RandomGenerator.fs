module Rushmallow.Cryptography.Primitives.RandomGenerator

open System.Security.Cryptography

open Rushmallow.Cryptography.Common


let private provider = new RNGCryptoServiceProvider()


let GenerateNumber : bigint = 
    let array = Array.zeroCreate Length
    provider.GetBytes array
    array |> bigint


let GenerateManyNumbers (count: int) : bigint list = 
    List.init count <| fun _ -> GenerateNumber
