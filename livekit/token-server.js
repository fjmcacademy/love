// Minimal development token service. Restrict access and add authentication before production.
const express = require('express');
const { AccessToken } = require('livekit-server-sdk');
const app = express(); app.use(express.json());
const KEY = process.env.LIVEKIT_API_KEY; const SECRET = process.env.LIVEKIT_API_SECRET;
if (!KEY || !SECRET) throw new Error('Set LIVEKIT_API_KEY and LIVEKIT_API_SECRET');
app.post('/token', async (req,res)=>{
  const {room, identity} = req.body || {};
  if(!room || !identity) return res.status(400).json({error:'room and identity required'});
  const at = new AccessToken(KEY, SECRET, {identity, ttl:'1h'});
  at.addGrant({roomJoin:true, room, canPublish:true, canSubscribe:true, canPublishData:true});
  res.json({token: await at.toJwt()});
});
app.listen(process.env.PORT||3000,()=>console.log('Token service listening'));
