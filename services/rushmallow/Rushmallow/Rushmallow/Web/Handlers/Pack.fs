module Rushmallow.Web.Handlers.Pack

open Suave
open Suave.DotLiquid

open Rushmallow.Storage.Helpers.Pack
open Rushmallow.Storage.Helpers.Marshmallow
open Rushmallow.Web.Contracts.Pack
open Rushmallow.Cryptography.SSS


[<Literal>]
let private DefaultFilling = "default"


let ShowAddMenu = page "pack/add.liquid" null


let ShowAll : WebPart = 
    page "pack/all.liquid" <| FindAllPacks


let Show (guid: string) : WebPart = 
    page "pack/single.liquid" <| FindSinglePack guid


let AddNew (request: CreatePackRequest) : CreatePackResponse =
    let error = {
        Success = false
        Error = "Please, use all fields!"
        Guid = null
        Sugar = null 
    }
    if isNull request.Name || isNull request.Flavour then error
    else
        let shift f x y z = f z x y
        let secrets = ExposeSecret request.Flavour
        let guids = secrets
                    |> Seq.skip 1
                    |> Seq.map (string >> (shift InsertSingleMarshmallow DefaultFilling false))
                    |> Seq.toList
        {
            Success = true
            Error = null
            Guid = InsertSinglePack request.Name guids
            Sugar = secrets |> Seq.first |> Option.get |> string
        }
