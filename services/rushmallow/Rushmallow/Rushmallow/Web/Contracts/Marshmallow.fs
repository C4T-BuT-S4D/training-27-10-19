module Rushmallow.Web.Contracts.Marshmallow

open System.Runtime.Serialization


[<DataContract>]
type CreateMarshmallowRequest = {
    [<field: DataMember(Name = "sugar")>]
    Sugar : string

    [<field: DataMember(Name = "filling")>]
    Filling: string
    
    [<field: DataMember(Name = "isPrivate")>]
    IsPrivate: bool
}


[<DataContract>]
type CreateMarshmallowResponse = {
    [<field: DataMember(Name = "success")>]
    Success: bool

    [<field: DataMember(Name = "error")>]
    Error: string

    [<field: DataMember(Name = "guid")>]
    Guid: string
}


[<DataContract>]
type ProveMarshmallowRequest = {
    [<field: DataMember(Name = "filling")>]
    Filling: string
}


[<DataContract>]
type ProveMarshmallowResponse = {
    [<field: DataMember(Name = "success")>]
    Success: bool

    [<field: DataMember(Name = "error")>]
    Error: string

    [<field: DataMember(Name = "filling")>]
    Filling: string
}
