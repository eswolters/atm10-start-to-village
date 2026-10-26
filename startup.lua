-- startup.lua : fill MineColonies requests from AE2
-- Needs: Advanced Computer + Colony Integrator + ME Bridge (Advanced Peripherals)
local colony = peripheral.find("colony_integrator") or peripheral.find("colonyIntegrator")
local me     = peripheral.find("me_bridge") or peripheral.find("meBridge")
assert(colony, "No Colony Integrator found")
assert(me, "No ME Bridge found")

local OUT      = "up"   -- side of the ME Bridge the Stash sits on
local WAIT     = 30     -- seconds between checks
local COOLDOWN = 300    -- seconds before re-sending the same request
local SKIP = {          -- items the colony should make itself
  ["minecraft:enchanted_book"] = true,
}

-- function names changed between Advanced Peripherals versions
local isCraftable = me.isCraftable or me.isItemCraftable
local isCrafting  = me.isCrafting  or me.isItemCrafting

local sentAt = {}  -- request id -> time we last handled it

local function stock(name)
  local item = me.getItem({ name = name })
  if type(item) ~= "table" then return 0 end
  return item.count or item.amount or 0
end

local function fill(req)
  local first = req.items and req.items[1]
  if not first or SKIP[first.name] then return end
  local name, need = first.name, req.count or 1
  local now = os.epoch("utc") / 1000
  if sentAt[req.id] and now - sentAt[req.id] < COOLDOWN then return end

  local have = stock(name)
  if have > 0 then
    local sent = me.exportItem({ name = name, count = math.min(have, need) }, OUT)
    if sent and sent > 0 then
      print(("Sent %d x %s for %s"):format(sent, name, req.target or "?"))
      sentAt[req.id] = now
    end
  elseif isCraftable and isCraftable({ name = name }) and not isCrafting({ name = name }) then
    me.craftItem({ name = name, count = need })
    print(("Crafting %d x %s"):format(need, name))
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