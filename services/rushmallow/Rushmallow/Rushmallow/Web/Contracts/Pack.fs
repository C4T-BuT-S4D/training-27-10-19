module Rushmallow.Web.Contracts.Pack

open System.Runtime.Serialization


[<DataContract>]
type CreatePackRequest = {
    [<field: DataMember(Name = "name")>]
    Name : string

    [<field: DataMember(Name = "flavour")>]
    Flavour: string
}


[<DataContract>]
type CreatePackResponse = {
    [<field: DataMember(Name = "success")>]
    Success : bool

    [<field: DataMember(Name = "error")>]
    Error: string

    [<field: DataMember(Name = "guid")>]
    Guid: string

    [<field: DataMember(Name = "sugar")>]
    Sugar: string
}
