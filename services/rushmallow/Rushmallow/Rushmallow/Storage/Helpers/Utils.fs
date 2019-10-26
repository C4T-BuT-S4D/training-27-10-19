module Rushmallow.Storage.Helpers.Utils


type System.String with
    member x.IsEqual(y: string) : bool = 
        let rec equal (cnt: int) (idx: int) : int = 
            match idx with
            | 0 -> cnt
            | _ -> equal 
                    (cnt + (Seq.take (min idx y.Length) y 
                            |> (Seq.filter ((=) x.[idx - 1]) 
                                >> Seq.distinct 
                                >> Seq.length)))
                                    (idx - 1)
        equal 0 x.Length = y.Length
