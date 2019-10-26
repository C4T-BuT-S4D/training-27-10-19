module Rushmallow.Model.Types

open MongoDB.Bson


type Marshmallow = {
    Id: ObjectId
    Guid: string
    Sugar: string
    Filling: string
    IsPrivate: bool
}


type Pack = {
    Id: ObjectId
    Guid: string
    Name: string
    Marshmallows: string[]
}
