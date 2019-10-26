module Rushmallow.Program

open System.IO

open Suave
open Suave.Json
open Suave.Filters
open Suave.Operators
open Suave.DotLiquid

open Rushmallow.Web.Handlers


let private config = { 
    defaultConfig with 
        bindings = [ HttpBinding.createSimple HTTP "0.0.0.0" 8080 ]
        homeFolder = Path.GetFullPath "static_files" |> Some 
}


let private routes = [
    GET >=> choose [ 
        path "/" >=> Other.ShowIndex

        path "/addPack" >=> Pack.ShowAddMenu
        path "/addMarshmallow" >=> Marshmallow.ShowAddMenu

        path "/packs" >=> Pack.ShowAll
        path "/marshmallows" >=> Marshmallow.ShowAll
        
        pathScan "/packs/%s" Pack.Show
        pathScan "/marshmallows/%s" Marshmallow.Show

        Files.browseHome
    ]
    
    POST >=> choose [ 
        path "/addPack" >=> mapJson Pack.AddNew
        path "/addMarshmallow" >=> mapJson Marshmallow.AddNew

        pathScan "/marshmallows/%s" (Marshmallow.Prove >> mapJson)
    ]

    RequestErrors.NOT_FOUND "Page not found."
]


[<EntryPoint>]
let main argv =
    setCSharpNamingConvention ()
    Path.GetFullPath "templates" |> setTemplatesDir
    startWebServer config (choose routes)
    0
