return {
    groups = {
        {
            name = "Models",
            children = {
                {
                    name = "Cassidy Herndon",
                    rules = {
                        {
                            field = "keywords",
                            op = "any",
                            value = "@casadilla1121",
                        },
                    },
                    children = {
                        {
                            name = "AbelCollab",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "AbelCollab",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                {
                    name = "Keri",
                    rules = {
                        {
                            field = "keywords",
                            op = "any",
                            value = "@kerielle777",
                        },
                    },
                    children = {
                        {
                            name = "Keri Visit",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Keri Visit",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                {
                    name = "Ubaid Family",
                    rules = {
                        {
                            field = "keywords",
                            op = "any",
                            value = "@ubaidrahman87",
                        },
                    },
                    children = {
                        {
                            name = "Ubaid Family",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Ubaid Family",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                {
                    name = "Valentina Reneff-Olson",
                    rules = {
                        {
                            field = "keywords",
                            op = "any",
                            value = "@vallady",
                        },
                    },
                    children = {
                        {
                            name = "Catwoman",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Catwoman",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                        {
                            name = "Westfield Shoot",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Westfield Shoot",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
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
                    name = "Hollywood",
                    rules = {
                        {
                            field = "location",
                            op = "==",
                            value = "Hollywood",
                        },
                    },
                    children = {
                        {
                            name = "Ubaid Family",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Ubaid Family",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                {
                    name = "Mount Tamalpais",
                    rules = {
                        {
                            field = "location",
                            op = "==",
                            value = "Mount Tamalpais",
                        },
                    },
                    children = {
                        {
                            name = "AbelCollab",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "AbelCollab",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                {
                    name = "Santa Monica Beach",
                    rules = {
                        {
                            field = "location",
                            op = "==",
                            value = "Santa Monica Beach",
                        },
                    },
                    children = {
                        {
                            name = "Keri Visit",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Keri Visit",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                        {
                            name = "Ubaid Family",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Ubaid Family",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                {
                    name = "The Huntington Library",
                    rules = {
                        {
                            field = "location",
                            op = "==",
                            value = "The Huntington Library",
                        },
                    },
                    children = {
                        {
                            name = "Keri Visit",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Keri Visit",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                {
                    name = "Walt Disney Concert Hall",
                    rules = {
                        {
                            field = "location",
                            op = "==",
                            value = "Walt Disney Concert Hall",
                        },
                    },
                    children = {
                        {
                            name = "Catwoman",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Catwoman",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                {
                    name = "Westfield Century City",
                    rules = {
                        {
                            field = "location",
                            op = "==",
                            value = "Westfield Century City",
                        },
                    },
                    children = {
                        {
                            name = "Westfield Shoot",
                            rules = {
                                {
                                    field = "jobIdentifier",
                                    op = "==",
                                    value = "Westfield Shoot",
                                },
                            },
                            smart = {
                                {
                                    name = "RAWs",
                                    rules = {
                                        {
                                            field = "fileFormat",
                                            op = "==",
                                            value = "RAW",
                                        },
                                    },
                                },
                                {
                                    name = "Rated",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = ">=",
                                            value = 1,
                                        },
                                    },
                                },
                                {
                                    name = "Five Star",
                                    rules = {
                                        {
                                            field = "rating",
                                            op = "==",
                                            value = 5,
                                        },
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
                    name = "AbelCollab",
                    rules = {
                        {
                            field = "jobIdentifier",
                            op = "==",
                            value = "AbelCollab",
                        },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                {
                                    field = "fileFormat",
                                    op = "==",
                                    value = "RAW",
                                },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                {
                                    field = "rating",
                                    op = ">=",
                                    value = 1,
                                },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                {
                                    field = "rating",
                                    op = "==",
                                    value = 5,
                                },
                            },
                        },
                    },
                },
                {
                    name = "Catwoman",
                    rules = {
                        {
                            field = "jobIdentifier",
                            op = "==",
                            value = "Catwoman",
                        },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                {
                                    field = "fileFormat",
                                    op = "==",
                                    value = "RAW",
                                },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                {
                                    field = "rating",
                                    op = ">=",
                                    value = 1,
                                },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                {
                                    field = "rating",
                                    op = "==",
                                    value = 5,
                                },
                            },
                        },
                    },
                },
                {
                    name = "GC Docs",
                    rules = {
                        {
                            field = "jobIdentifier",
                            op = "==",
                            value = "GC Docs",
                        },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                {
                                    field = "fileFormat",
                                    op = "==",
                                    value = "RAW",
                                },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                {
                                    field = "rating",
                                    op = ">=",
                                    value = 1,
                                },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                {
                                    field = "rating",
                                    op = "==",
                                    value = 5,
                                },
                            },
                        },
                    },
                },
                {
                    name = "Keri Visit",
                    rules = {
                        {
                            field = "jobIdentifier",
                            op = "==",
                            value = "Keri Visit",
                        },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                {
                                    field = "fileFormat",
                                    op = "==",
                                    value = "RAW",
                                },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                {
                                    field = "rating",
                                    op = ">=",
                                    value = 1,
                                },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                {
                                    field = "rating",
                                    op = "==",
                                    value = 5,
                                },
                            },
                        },
                    },
                },
                {
                    name = "MacBookPro",
                    rules = {
                        {
                            field = "jobIdentifier",
                            op = "==",
                            value = "MacBookPro",
                        },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                {
                                    field = "fileFormat",
                                    op = "==",
                                    value = "RAW",
                                },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                {
                                    field = "rating",
                                    op = ">=",
                                    value = 1,
                                },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                {
                                    field = "rating",
                                    op = "==",
                                    value = 5,
                                },
                            },
                        },
                    },
                },
                {
                    name = "PassportScan",
                    rules = {
                        {
                            field = "jobIdentifier",
                            op = "==",
                            value = "PassportScan",
                        },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                {
                                    field = "fileFormat",
                                    op = "==",
                                    value = "RAW",
                                },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                {
                                    field = "rating",
                                    op = ">=",
                                    value = 1,
                                },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                {
                                    field = "rating",
                                    op = "==",
                                    value = 5,
                                },
                            },
                        },
                    },
                },
                {
                    name = "Ubaid Family",
                    rules = {
                        {
                            field = "jobIdentifier",
                            op = "==",
                            value = "Ubaid Family",
                        },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                {
                                    field = "fileFormat",
                                    op = "==",
                                    value = "RAW",
                                },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                {
                                    field = "rating",
                                    op = ">=",
                                    value = 1,
                                },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                {
                                    field = "rating",
                                    op = "==",
                                    value = 5,
                                },
                            },
                        },
                    },
                },
                {
                    name = "Westfield Shoot",
                    rules = {
                        {
                            field = "jobIdentifier",
                            op = "==",
                            value = "Westfield Shoot",
                        },
                    },
                    smart = {
                        {
                            name = "RAWs",
                            rules = {
                                {
                                    field = "fileFormat",
                                    op = "==",
                                    value = "RAW",
                                },
                            },
                        },
                        {
                            name = "Rated",
                            rules = {
                                {
                                    field = "rating",
                                    op = ">=",
                                    value = 1,
                                },
                            },
                        },
                        {
                            name = "Five Star",
                            rules = {
                                {
                                    field = "rating",
                                    op = "==",
                                    value = 5,
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}
