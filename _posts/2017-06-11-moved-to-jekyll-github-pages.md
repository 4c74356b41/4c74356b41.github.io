---
id: 5772
title: Moved to Github Pages and Jekyll
date: 2017-06-11T21:40:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5772
permalink: /post5772
categories:
  - random
---

I was using Project Nami and Azure SQL for my wordpress, but I decided against that as I don't need all that mess, so I moved to Github Pages and Jekyll. I now have a static webpage, less management and, theoretically, people can submit PR's to fix my stuff ;)

Process\Issues:  
1. Project Nami and Jekyll exporter do not play well together (at all), so I had to export all the data using wordpress export and import it to a fresh wordpress install ([using docker-compose](https://docs.docker.com/compose/wordpress/))
2. Installed and used Jekyll exporter plugin (which didn't exactly work, but it created temp files in `/tmp`, so I went into the container and tared them and downloaded over the http server)
3. Followed [this article](https://www.smashingmagazine.com/2014/08/build-blog-jekyll-github-pages/)
4. Found lots of small bugs\inconsistencies and fixed them for several hours (and probably next several days; actually still fixing)

<strike>A really big issue, my blog used permalinks like this: "?p=xxxx" and Jekyll fails to use that. No ideas about how to fix this, so I worked around by searching\replacing "?p=" to "post". Kinda works. I hope google catches up at some point.</br>
Maybe worth looking at [this](https://github.com/jekyll/jekyll-redirect-from) later.<br><br>

Meanwhile, if you found this in google and it redirects you to the main page instead of the post you are looking for just do a search for the post name on the main page with `Ctrl+F`.</strike>

update 26.06.2017:  
Apparently Jekyll redirect cannot help with my trouble. So I've used sitemap.xml and google webmaster console to reindex the site, I don't know if it hurts my SEO, but well, nothing I can do.  
I've spent a last few days fighting css and fixing a logo\icon for meself. Its not that css is hard, I just rarely use that, so its a bit hard to get into it everytime I have to do it again ;)

So I guess I'm happier now. Best of luck folks.
