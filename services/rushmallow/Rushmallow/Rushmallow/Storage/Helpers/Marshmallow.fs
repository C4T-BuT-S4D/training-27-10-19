module Rushmallow.Storage.Helpers.Marshmallow

open System
open System.Collections.Generic

open MongoDB.Bson
open MongoDB.Driver

open Rushmallow.Model.Types
open Rushmallow.Storage.MongoDB


let FindAllMarshmallows : IEnumerable<Marshmallow> =
    marshmallowsCollection
        .Find<Marshmallow>(Builders.Filter.Empty)
        .ToEnumerable()


let FindSingleMarshmallow (guid: string) : Marshmallow = 
    marshmallowsCollection
        .Find<Marshmallow>(fun m -> m.Guid = guid)
        .FirstOrDefault()


let InsertSingleMarshmallow (sugar: string) (filling: string) (isPrivate: bool) : string = 
    let marshmallow = {
        Id = ObjectId.GenerateNewId()
        Guid = Guid.NewGuid().ToString()
        Sugar = sugar
        Filling = filling
        IsPrivate = isPrivate
    }
    marshmallowsCollection.InsertOne(marshmallow)
    marshmallow.Guid
