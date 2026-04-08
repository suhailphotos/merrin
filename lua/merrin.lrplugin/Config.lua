return {
    groups = {
        {
            name = "Models",
            children = {
                {
                    name = "Valentina Reneff-Olson",
                    rules = {
                        { field = "keywords", op = "contains", value = "@vallady" },
                    },
                    children = {
                        {
                            name = "Catwoman",
                            rules = {
                                { field = "searchableIptc", op = "contains", value = "Catwoman" },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    match = "all",
                                    rules = {
                                        { field = "fileType", op = "is", value = "Raw" },
                                    },
                                },
                                {
                                    name = "Rated",
                                    match = "all",
                                    rules = {
                                        { field = "rating", op = ">=", value = 1 },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    match = "all",
                                    rules = {
                                        { field = "rating", op = "==", value = 5 },
                                    },
                                },
                                {
                                    name = "Edits",
                                    match = "any",
                                    rules = {
                                        { field = "fileType", op = "is", value = "TIFF" },
                                        { field = "fileType", op = "is", value = "PSD" },
                                        { field = "fileType", op = "is", value = "PSB" },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}
