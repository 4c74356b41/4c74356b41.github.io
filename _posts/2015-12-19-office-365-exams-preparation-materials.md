---
id: 4423
title: Office 365 exams preparation materials
date: 2015-12-19T14:28:48+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post4423
permalink: /post4423
categories:
  - random
tags:
  - Office365
---
General.

[Fasttrack](http://fasttrack.office.com/)
  
[Planning and Design](https://www.microsoft.com/en-us/download/details.aspx?id=732)
  
[Office 365 for IT Pros](https://technet.microsoft.com/en-us/office/dn788774)
  
[Office 365 IT Pro Blog](https://blogs.technet.microsoft.com/office_resource_kit/)
  
[Office 365 Service Descriptions](https://technet.microsoft.com/library/jj819284.aspx)

[Exam 347 page](https://www.microsoft.com/en-us/learning/exam-70-347.aspx) ([Getting ready videos ch9](https://channel9.msdn.com/Blogs/mcpexamprep/70-347-Enabling-Office-365-Services))
  
[Exam 346 page](https://www.microsoft.com/en-us/learning/exam-70-346.aspx) ([Getting ready videos ch9](https://channel9.msdn.com/Blogs/mcpexamprep/70-346-Managing-Office-365-Identities-and-Requirements))
  
[MVA page](https://mva.microsoft.com/product-training/office-365)

[Exchange Deployment Assistant](https://technet.microsoft.com/en-us/exdeploy2013/Checklist?state=2718-W-AAAAAAAAQAAAAAEAAAAAAAAAAAAA)

<p align="left">
  DNS.<br /> <a href="https://technet.microsoft.com/en-us/library/aa996295(v=exchg.150).aspx">SenderID</a>
</p>

Network.
  
[NAT support](https://msdn.microsoft.com/en-us/library/dn850366.aspx), [Performance Tuning](https://mva.microsoft.com/en-US/training-courses/office-365-performance-management-8416?l=webmRJKz_7104984382), [DNS Records](https://support.office.com/en-us/article/External-Domain-Name-System-records-for-Office-365-c0531a6f-9e25-4f2d-ad0e-a70bfef09ac0?ui=en-US&rs=en-US&ad=US) ([Windows Based](https://support.office.com/en-us/article/Create-DNS-records-for-Office-365-using-Windows-based-DNS-9EEC911D-5773-422C-9593-40E1147FFBDE?ui=en-US&rs=en-US&ad=US)), [URLs and IP Ranges](https://support.office.com/en-us/article/Office-365-URLs-and-IP-address-ranges-8548a211-3fe7-47cb-abb1-355ea5aa88a2?ui=en-US&rs=en-US&ad=US), [SFB Network Setup](https://support.office.com/en-us/article/Set-up-your-network-for-Skype-for-Business-Online-81fa5e16-418d-4698-a5f0-e666211c5c66?CorrelationId=d521b776-b90c-4cd3-8b2a-97d1b08c4856&ui=en-US&rs=en-US&ad=US#__step_two__configure),
  
Calculators:
  
[SFB](https://www.microsoft.com/en-us/download/details.aspx?id=19011) ([additional reference](https://technet.microsoft.com/en-us/library/gg413004%28v=ocs.14%29.aspx)), [Exchange Client](https://gallery.technet.microsoft.com/Exchange-Client-Network-8af1bf00), [Sharepoint (kinda)](https://technet.microsoft.com/en-us/library/cc262952(v=office.12).aspx), [OneDrive](https://www.microsoft.com/en-us/download/details.aspx?id=44541), [ADFS](https://www.microsoft.com/en-us/download/details.aspx?id=2278)

Misc.
  
[RMS Sharing Quick Start](https://technet.microsoft.com/en-us/library/mt126254.aspx), [Configure Apps for RMS](https://technet.microsoft.com/en-us/library/jj585031.aspx), [SFB Hybrid](https://technet.microsoft.com/en-us/library/jj205403.aspx), [Office Deployment Tool for Click-to-Run](https://technet.microsoft.com/en-us/library/jj219422(v=office.15))

Troubleshooting.
  
[Connectivity Analyzer](https://testconnectivity.microsoft.com/), [Client Performance Analyzer](https://support.office.com/en-us/article/Office-365-Client-Performance-Analyzer-e16b0928-bd38-423b-bd4e-b8402bc106aa), [NetMon 3.4](https://www.microsoft.com/en-us/download/details.aspx?id=4865), [Message Analyzer 1.0](https://www.microsoft.com/en-us/download/details.aspx?id=40308), [Office 365 Troubleshooter](https://community.office365.com/en-us/p/troubleshooting#31609269-0), [Diagnostics Tools](https://community.office365.com/en-us/w/diagnostic_tools/), [Free/Busy Hybeis Troubleshooter](https://support2.microsoft.com/common/survey.aspx?scid=sw;en;3526&showpage=1&viewproduction=1),

Powershell.
  
[Azure AD Powershell](https://technet.microsoft.com/en-us/library/jj151815.aspx) ([Prerequisite for O365 Powershell Modules](https://www.microsoft.com/en-us/download/details.aspx?id=41950))([examples](https://technet.microsoft.com/en-us/library/dn568002.aspx))([download](http://go.microsoft.com/fwlink/p/?linkid=236297))
  
[Azure RMS Powershell](https://technet.microsoft.com/en-us/library/jj585012.aspx) ([download](https://www.microsoft.com/en-us/download/details.aspx?id=30339))
  
[SFB Powershell](https://technet.microsoft.com/en-us/library/dn362817(v=ocs.15).aspx) ([download](http://www.microsoft.com/en-us/download/details.aspx?id=39366))
  
[Sharepoint Powershell](https://technet.microsoft.com/en-us/library/fp161374.aspx)  ([download](http://www.microsoft.com/en-us/download/details.aspx?id=35588))

```
#Don’t forget Execution Policy
#Office365
Connect-MsolService
#Exchange Online
$session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri https://ps.outlook.com/powershell -Credential (Get-Credential) -Authentication Basic -AllowRedirection
Import-PSSession $session
#RMS with basic setup
Connect-aadrmservice
Set-IRMConfiguration -RMSOnlineKeySharingLocation "https://sp-rms.eu.aadrm.com/TenantManagement/ServicePartner.svc" 
Import-RMSTrustedPublishingDomain -RMSOnline -name "RMS Online"
Set-IRMConfiguration –InternalLicensingEnabled $true
Test-IRMConfiguration –RMSOnline
#SFB
$session = New-CsOnlineSession -Credential (Get-Credential)
Import-PSSession $session
#Sharepoint
Connect-SPOService -Url https://COMPANYNAME-admin.sharepoint.com -Credential (Get-Credential)
```