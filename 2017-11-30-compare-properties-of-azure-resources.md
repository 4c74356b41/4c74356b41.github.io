---
id: 5776
title: SQL Server 2016 AlwaysOn automated deployment on Azure
date: 2017-11-30T11:40:00+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post5776
permalink: /post5776
categories:
  - Azure
  - Powershell
---

Howdy,

I needed a function to quickly compare object properties of Azure resources. So i came up with these.
They might not work with objects that are many levels deep, but they seem to work well for 2-3 levels deep objects.
I think it covers most of the objects in Azure.

Usage:
1. Import both functions into session
2. Run the 'meta' function and pass objects to compare to it: 'Compare-AzureObject $firstObject $secondObject'
3. Examine on screen output, log.txt and error.txt if any exist.

```powershell
Function Compare-ObjectProperties {
    Param(
        [PSObject]$refObject,
        [PSObject]$difObject,
        [string]$propertyName
    )

    try {
        if ( $refObject.Count -eq 0 -and $difObject.Count -eq 0 ) { "INFO: Nothing to compare, both properties are null ($propertyName)" >> log.txt; return }
        $objprops = $refObject | Get-Member -MemberType Property, NoteProperty -ErrorAction SilentlyContinue | ForEach-Object Name
        $objprops += $difObject | Get-Member -MemberType Property, NoteProperty -ErrorAction SilentlyContinue | ForEach-Object Name
        $objprops = $objprops | Sort-Object | Select-Object -Unique
        $diffs = @()
        foreach ($objprop in $objprops) {
            # skipping "useless" comparisons
            if ($objprop -in ('id', 'etag', 'resourceguid') -or $objprop -like '*text') { continue }
            $diff = Compare-Object $refObject $difObject -Property $objprop
            if ($diff) {            
                $diffprops = @{
                    PropertyName   = $objprop
                    ParentProperty = $propertyName
                    RefValue       = ($diff | Where-Object {$_.SideIndicator -eq '<='} | ForEach-Object $($objprop))
                    DiffValue      = ($diff | Where-Object {$_.SideIndicator -eq '=>'} | ForEach-Object $($objprop))
                }
                $diffs += New-Object PSObject -Property $diffprops
            }        
        }
        if ($diffs) { 
            return ( $diffs )
        }
        else {
            "INFO: properties are equal or skipped ($propertyName)" >> log.txt 
        }
    }
    catch {
        "ERROR: something went wrong with $propertyName" >> log.txt
        $_ >> errors.txt
    }
}

Function Compare-AzureObjects {
    Param(
        [Parameter(Mandatory)]
        $firstObject,
        [Parameter(Mandatory)]
        $secondObject
    )
    $firstObject | Get-Member -MemberType Property | Where-Object { $PSItem.Name -notlike '*text' } | ForEach-Object {
        $propertyName = $_.Name
        $data = Compare-ObjectProperties $firstObject.($propertyName) $secondObject.($propertyName) $propertyName
        if ($data) {
            $data | Format-Table @{n = "Parent Property"; e = {$_.ParentProperty}}, @{n = "Child Property"; e = {$_.PropertyName}}, @{n = $firstObject.Name; e = {$_.RefValue}}, @{n = $secondObject.Name; e = {$_.DiffValue}} -Wrap
        }
    }
}
```
