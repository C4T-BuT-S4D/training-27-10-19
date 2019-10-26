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
    let marshmallow = FindSingleMarshmallow guid
    if isNull <| box marshmallow || marshmallow.IsPrivate then
        page "marshmallow/private.liquid" marshmallow
    else
        page "marshmallow/single.liquid" marshmallow 


let Prove (guid: string) (request: ProveMarshmallowRequest) : ProveMarshmallowResponse = 
    let error = {
        Success = false
        Error = "Please, use all fields!"
        Filling = null
    }
    if isNull request.Filling then error
    else
        let marshmallow = FindSingleMarshmallow guid
        if request.Filling.IsEqual(marshmallow.Filling) then 
            {
                Success = true
                Error = null
                Filling = marshmallow.Filling
            } 
        else 
            {
                Success = false
                Error = "Incorrect filling."
                Filling = null
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
 