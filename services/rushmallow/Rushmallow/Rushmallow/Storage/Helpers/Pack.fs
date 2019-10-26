module Rushmallow.Storage.Helpers.Pack

open System
open System.Collections.Generic

open MongoDB.Bson
open MongoDB.Driver

open Rushmallow.Model.Types
open Rushmallow.Storage.MongoDB


let FindAllPacks : IEnumerable<Pack> =
    packsCollection
        .Find<Pack>(Builders.Filter.Empty)
        .ToEnumerable()


let FindSinglePack (guid: string) : Pack = 
    packsCollection
        .Find<Pack>(fun p -> p.Guid = guid)
        .FirstOrDefault()


let InsertSinglePack (name: string) (marshmallows: IEnumerable<string>) : string = 
    let pack = {
        Id = ObjectId.GenerateNewId()
        Guid = Guid.NewGuid().ToString()
        Name = name
        Marshmallows = marshmallows |> Seq.toArray
    }
    packsCollection.InsertOne(pack)
    pack.Guid
