local LrDialogs = import "LrDialogs"
local LrTasks = import "LrTasks"

local Smart = dofile(_PLUGIN.path .. "/Smart.lua")

LrTasks.startAsyncTask(function()
    local ok, err = LrTasks.pcall(function()
        Smart.run()
    end)

    if not ok then
        LrDialogs.message(
            "Merrin",
            "Error:\n" .. tostring(err),
            "critical"
        )
    end
end)
