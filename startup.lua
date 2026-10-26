-- startup.lua : fill MineColonies requests from AE2
-- Needs: Advanced Computer + Colony Integrator + ME Bridge (Advanced Peripherals)
local colony = peripheral.find("colony_integrator")
local me     = peripheral.find("me_bridge")
assert(colony, "No Colony Integrator found")
assert(me, "No ME Bridge found")

-- Where the items go. "@up" is the inventory directly above the ME Bridge (the Stash).
-- Other sides: "@down", "@north", "@south", "@east", "@west", or "@front", "@back", "@left",
-- "@right", "@top", "@bottom" relative to the bridge. Without the @ it is the name of a
-- peripheral on a wired modem network, for example "minecolonies:stash_0".
local OUT      = "@up"
local WAIT     = 30     -- seconds between checks
local COOLDOWN = 300    -- seconds before re-sending the same request
local SKIP = {          -- items the colony should make itself
  ["minecraft:enchanted_book"] = true,
}

local sentAt = {}  -- request id -> time we last handled it

local function stock(name)
  local item = me.getItem({ name = name })
  if type(item) ~= "table" then return 0 end
  return item.count or item.amount or 0
end

-- Advanced Peripherals 0.8 takes (destination, filter). Older versions took (filter, direction).
local function export(name, count)
  local filter = { name = name, count = count }
  local ok, sent, err = pcall(me.exportItem, OUT, filter)
  if ok then return sent, err end
  local ok2, sent2, err2 = pcall(me.exportItem, filter, (OUT:gsub("^@", "")))
  if ok2 then return sent2, err2 end
  return nil, tostring(sent)
end

local function fill(req)
  local first = req.items and req.items[1]
  if not first or SKIP[first.name] then return end
  local name, need = first.name, req.count or 1
  local label = req.displayName or first.displayName or name
  local now = os.epoch("utc") / 1000
  if sentAt[req.id] and now - sentAt[req.id] < COOLDOWN then return end

  local have = stock(name)
  if have > 0 then
    local sent, err = export(name, math.min(have, need))
    if sent and sent > 0 then
      print(("Sent %d x %s for: %s"):format(sent, name, label))
      sentAt[req.id] = now
    else
      print(("Could not send %s: %s"):format(name, tostring(err or "nothing moved (is the Stash full or missing?)")))
    end
  elseif me.isCraftable({ name = name }) and not me.isCrafting({ name = name }) then
    me.craftItem({ name = name, count = need })
    print(("Crafting %d x %s for: %s"):format(need, name, label))
    sentAt[req.id] = now - COOLDOWN + WAIT * 2  -- check again soon
  end
end

while true do
  local ok, requests = pcall(colony.getRequests)
  if ok and type(requests) == "table" then
    for _, req in ipairs(requests) do
      local ok2, err = pcall(fill, req)
      if not ok2 then print("Error: " .. tostring(err)) end
    end
  else
    print("Could not read requests: " .. tostring(requests))
  end
  sleep(WAIT)
end
