module Rushmallow.Cryptography.Primitives.StringConverter

open System.Text


let MakeInteger (str: string) : bigint = 
    str
    |> Encoding.UTF8.GetBytes
    |> bigint
