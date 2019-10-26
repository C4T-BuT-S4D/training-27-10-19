module Rushmallow.Web.Handlers.Marshmallow
    
open Suave
open Suave.DotLiquid

open Rushmallow.Storage.Helpers.Utils
open Rushmallow.Storage.Helpers.Marshmallow
open Rushmallow.Web.Contracts.Marshmallow
    

let ShowAddMenu = page "marshmallow/add.liquid" null
    
    
let ShowAll : WebPart = 
    page "marshmallow/all.liquid" <| FindAllMarshmallows
    
    
let Show (guid: string) : WebPart = 
    page "marshmallow/single.liquid" <| FindSingleMarshmallow guid


let Prove (guid: string) (request: ProveMarshmallowRequest) : ProveMarshmallowResponse = 
    let error = {
        Success = false
        Error = "Please, use all fields!"
    }
    if isNull request.Filling then error
    else
        let marshmallow = FindSingleMarshmallow guid
        if request.Filling.IsEqual(marshmallow.Filling) then 
            {
                Success = true
                Error = null
            } 
        else 
            {
                Success = false
                Error = "Incorrect password."
            }


let AddNew (request: CreateMarshmallowRequest) : CreateMarshmallowResponse =
    let error = {
        Success = false
        Error = "Please, use all fields!"
        Guid = null
    }
    if isNull request.Filling || isNull request.Sugar then error
    else {
        Success = true
        Error = null
        Guid = InsertSingleMarshmallow request.Sugar request.Filling request.IsPrivate
    }
 