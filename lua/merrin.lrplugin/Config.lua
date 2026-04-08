return {
    groups = {
        {
            name = "Models",
            children = {
                {
                    name = "Valentina Reneff-Olson",
                    rules = {
                        { field = "keywords", op = "any", value = "@vallady" },
                    },
                    children = {
                        {
                            name = "Catwoman",
                            rules = {
                                { field = "iptc", op = "any", value = "Catwoman" },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        { field = "fileFormat", op = "==", value = "RAW" },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        { field = "rating", op = ">=", value = 1 },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        { field = "rating", op = "==", value = 5 },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },

        {
            name = "Locations",
            children = {
                {
                    name = "Walt Disney Concert Hall",
                    rules = {
                        { field = "iptc", op = "any", value = "Walt Disney Concert Hall" },
                    },
                    children = {
                        {
                            name = "Catwoman",
                            rules = {
                                { field = "iptc", op = "any", value = "Catwoman" },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        { field = "fileFormat", op = "==", value = "RAW" },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        { field = "rating", op = ">=", value = 1 },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        { field = "rating", op = "==", value = 5 },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },

        {
            name = "Projects",
            children = {
                {
                    name = "Catwoman",
                    rules = {
                        { field = "jobIdentifier", op = "==", value = "Catwoman" },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                { field = "fileFormat", op = "==", value = "RAW" },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                { field = "rating", op = ">=", value = 1 },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                { field = "rating", op = "==", value = 5 },
                            },
                        },
                    },
                },
            },
        },
    },
}
