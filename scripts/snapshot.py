"""Fetch open Kalshi events+markets (public API, no auth) -> data/markets.json (normalized to cents)."""
import json, time, urllib.request, datetime, os
B="https://api.elections.kalshi.com/trade-api/v2"
def get(u):
    r=urllib.request.Request(u,headers={"User-Agent":"kalshi-desk-snapshot"})
    return json.load(urllib.request.urlopen(r,timeout=30))
def c(x):
    try: return round(float(x)*100,2) if x not in (None,"") else None
    except: return None
def f(x):
    try: return float(x) if x not in (None,"") else 0.0
    except: return 0.0
out=[];cur="";pages=0
while pages<15:
    d=get(f"{B}/events?status=open&limit=200&with_nested_markets=true"+(f"&cursor={cur}" if cur else ""))
    for e in d.get("events",[]):
        for m in e.get("markets") or []:
            if m.get("status") not in ("active","open"): continue
            bid,ask=c(m.get("yes_bid_dollars")),c(m.get("yes_ask_dollars"))
            bs,as_=f(m.get("yes_bid_size_fp")),f(m.get("yes_ask_size_fp"))
            out.append(dict(ticker=m["ticker"],event_ticker=e["event_ticker"],series_ticker=e.get("series_ticker",""),
              category=e.get("category",""),title=m.get("title") or e.get("title"),event_title=e.get("title"),
              subtitle=m.get("yes_sub_title") or e.get("sub_title",""),yes_bid=bid,yes_ask=ask,
              no_bid=c(m.get("no_bid_dollars")),no_ask=c(m.get("no_ask_dollars")),last_price=c(m.get("last_price_dollars")),
              previous_price=c(m.get("previous_price_dollars")),volume=f(m.get("volume_fp")),volume_24h=f(m.get("volume_24h_fp")),
              open_interest=f(m.get("open_interest_fp")),
              liquidity=round((bid or 0)/100*bs+(100-(ask or 100))/100*as_,2),  # top-of-book $ depth (API no longer returns liquidity)
              close_time=m.get("close_time")))
    cur=d.get("cursor");pages+=1
    if not cur: break
    time.sleep(0.3)
tot=len(out)
out=[m for m in out if (m["yes_bid"] or 0)>0 and (m["yes_ask"] or 100)<100 and (m["volume_24h"]>0 or m["open_interest"]>0)]
out.sort(key=lambda m:-m["volume_24h"]); out=out[:2500]
os.makedirs("data",exist_ok=True)
json.dump({"fetched_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source":B+"/events?status=open&with_nested_markets=true","count":len(out),"scanned_open":tot,"markets":out},open("data/markets.json","w"),separators=(",",":"))
print(len(out),"markets")
