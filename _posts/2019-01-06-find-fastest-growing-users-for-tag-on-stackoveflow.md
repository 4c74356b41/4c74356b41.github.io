---
id: 5780
title: Finding fastest growing users for tag on stackoveflow
date: 2019-01-06T19:10:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5780
permalink: /post5780
categories:
  - stackoverflow
---

Howdy,

I got interested in how well do i stack up "against" other fellow SO users. Turns out - not too bad. I'm consistently top 3 over the last 3\2\1 years time frame :). Query:

```
select top 30 u.id as [User Link],  
       u.WebsiteUrl,
       t.TagName,
       sum(score) totscore
from Posts p, PostTags pt, Tags t, Users u
where p.CreationDate > DATEADD(year,##years:int?-3##,GETDATE())
AND PostTypeId = 2 -- answer
AND p.ParentId = pt.PostId
AND pt.TagId = t.id
AND p.OwnerUserId = u.id
AND t.TagName = ##tag:string?azure##
group by u.id, 
         u.WebsiteUrl,
         t.TagName
order by totscore desc
```

ps. [SO database schema](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede).

Happy deploying!