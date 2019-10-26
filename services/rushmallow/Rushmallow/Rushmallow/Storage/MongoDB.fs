module Rushmallow.Storage.MongoDB

open MongoDB.Driver

open Rushmallow.Model.Types


[<Literal>]
let private ConnectionString = "mongodb://127.0.0.1:27017"

[<Literal>]
let private DatabaseName = "rushmallow"

[<Literal>]
let private PackCollectionName = "packs"
[<Literal>]
let private MarshmallowCollectionName = "marshmallows"


let private database = MongoClient(ConnectionString).GetDatabase(DatabaseName)

let packsCollection = database.GetCollection<Pack>(PackCollectionName)
let marshmallowsCollection = database.GetCollection<Marshmallow>(MarshmallowCollectionName)
