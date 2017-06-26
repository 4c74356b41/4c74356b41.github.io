---
id: 546
title: '"Сердце" PDT - Variable.xml (часть 1)'
date: 2014-06-19T23:45:07+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post546
permalink: /post546
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Guide
  - PDT
  - PDT GUI
  - Powershell Deployment Toolkit
  - System Center 2012 R2
  - Windows Azure Pack
---
В продолжении предыдущего поста про <a href="http://4c74356b41.com/post485">Powershell Deployment Toolkit</a>, займемся изучением Variable.xml.

Чтож, начнем с изучения коротенького Variable.xml:
```
<?xml version="1.0" encoding="utf-8"?>

<Installer version="2.0">
  <Variable Name="SystemCenter2012ProductKey" Value="Ключ" /> – Ключ, который будет использоваться при установке компонентов System Center.
  <Variable Name="SQLServer2012ProductKey" Value="Ключ" /> – Ключ, который будет использоваться при установке SQL Server 2012.
  <Variable Name="SQLServer2008R2ProductKey" Value="Ключ" /> – Ключ, который будет использоваться при установке SQL Server 2008 R2.
  <Variable Name="RegisteredUser" Value="Microsoft Corporation" /> – Имя пользователя, которое будет использоваться на странице регистрации продукта.
  <Variable Name="RegisteredOrganization" Value="Microsoft Corporation" /> – Имя компании, которое будет использоваться на странице регистрации продукта.
  <Variable Name="InstallerServiceAccount" Value="CONTOSO!Installer" /> – Аккаунт от имени которого будет происходить установка всех компонентов System Center и Windows Azure Pack.
  <Variable Name="InstallerServiceAccountPassword" Value="!Q2w3e4r" /> – Пароль от аккаунта.
  <Variable Name="SourcePath" Value="$SystemDriveInstaller" /> – Путь, по которому скрипт VMCreator.ps1 будет копировать, а Installer.ps1 будет искать файлы зависимостей. В ходе экспериментов удалось установить что "$SystemDrive" крайне желательно не трогать.
  <Variable Name="Download" Value="C:Installer" /> – Путь, по которому VMCreator.ps1 будет искать файлы зависимостей, чтобы скопировать их на виртуальные машины.
  <Variable Name="MicrosoftUpdate" Value="1" /> – Использовать ли Microsoft Update (0 или 1).
  <Variable Name="CustomerExperienceImprovementProgram" Value="1" /> – Вступать ли в CEIP (0 или 1).
  <Variable Name="ErrorReporting" Value="1" /> – Отправлять ли отчеты об ошибках в Microsoft (0 или 1).
На этом "глобальные переменные" заканчиваются. Кроме описаных выше есть еще 2 переменные (TempPath и OperationalDataReporting), о которых я не смог найти какого-либо описания, но на практике они не нужны. Все работает даже без последних трех переменных, а в случае если Вы не укажите первые три, все компоненты будут поставлены в ознакомительном режиме (их тоже можно удалить из Variable.xml).

 

  <Components> – описание компонентов System Center и Windows Azure Pack, которые будут установлены.
    <Component Name="System Center 2012 R2 Virtual Machine Manager"> – описание VMM.
      <Variable Name="SystemCenter2012R2VirtualMachineManagerProgramFiles" Value="D:Program FilesMicrosoft System Center 2012 R2Virtual Machine Manager" /> – Путь, по которому будет установлен VMM.
      <Variable Name="SystemCenter2012R2VirtualMachineManagerAdminGroup" Value="CONTOSOVMM-Admins" /> – Группа администраторов VMM.
      <Variable Name="SystemCenter2012R2VirtualMachineManagerBitsTcpPort" Value="444" /> – Порт, который будет использовать VMM для операций с использованием службы BITS.
      <Variable Name="SystemCenter2012R2VirtualMachineManagerServiceAccount" Value="CONTOSO!vmm" /> – Сервисный аккаунт VMM.
      <Variable Name="SystemCenter2012R2VirtualMachineManagerServiceAccountPassword" Value="!Q2w3e4r" /> – Пароль от аккаунта.
    </Component>
  </Components>
На этом компоненты заканчиваются. Естественно их может быть (и скорее всего в ваших разворачиваниях будет) гораздо больше. Как же узнать как корректно добавить новые компоненты. Можно посмотреть вот сюда.

 

  <Roles> – описание ролей.
    <Role Name="System Center 2012 R2 Virtual Machine Manager Database Server" Server="SQL-01.contoso.com" Instance="MSSQLSERVER"></Role> – Сервер с базой данных VMM.
    <Role Name="SQL Server 2012 Management Tools" Server="SQL-01.contoso.com"></Role> – Management Tools для SQL сервера.
    <Role Name="System Center 2012 R2 Virtual Machine Manager Management Server" Server="VMM-01.contoso.com"></Role> – сервер управления VMM.
    <Role Name="System Center 2012 R2 Virtual Machine Manager Console" Server="VMM-01.contoso.com"></Role> – Сервер на который будет установлена консоль VMM.
  </Roles>
В этой части Variable.xml Вам просто нужно перечислить куда устанавливать все те компоненты что Вы указали в "зоне" компонентов

 

  <SQL> – описание инстансов SQL, которые будут созданы при разворачивании.
    <Instance Server="SQL-01.contoso.com" Instance="MSSQLSERVER" Version="SQL Server 2012"> – сервер для инстанса, версия SQL сервера и имя инстанса.
      <Variable Name="SQLAdmins" Value="CONTOSOSQL-Admins" /> – группа администраторов SQL сервера.
      <Variable Name="SQLInstallSQLDataDir" Value="D:Program FilesMicrosoft SQL Server" /> – каталог, куда будет произведена установка SQL сервера.
      <Variable Name="SQLUserDBDir" Value="D:MSSQL11.$InstanceMSSQLData" /> – каталог, где будут расположены базы данных.
      <Variable Name="SQLUserDBLogDir" Value="E:MSSQL11.$InstanceMSSQLData" /> – каталог, где будут расположены логи баз данных.
      <Variable Name="SQLTempDBDir" Value="F:MSSQL11.$InstanceMSSQLData" /> – каталог, где будет расположена TempDB.
      <Variable Name="SQLTempDBLogDir" Value="F:MSSQL11.$InstanceMSSQLData" /> – каталог, где будут расположены логи TempDB.
      <Variable Name="SQLAgtServiceAccount" Value="CONTOSO!sql" /> – Сервисный аккаунт сервиса SQL Agent.
      <Variable Name="SQLAgtServiceAccountPassword" Value="!Q2w3e4r" /> – Пароль от аккаунта.
      <Variable Name="SQLServiceAccount" Value="CONTOSO!sql" /> – Сервисный аккаунт сервиса SQL Engine.
      <Variable Name="SQLServiceAccountPassword" Value="!Q2w3e4r" /> – Пароль от аккаунта.
    </Instance>
  </SQL>
Если необходимо больше одного инстанса, нужно будет задать их создав еще 1-2-3 подобных конфигураций, начиная с <Instance Server bla-bla-bla> и до </Instance>. Таким образом, все инстансы должны находиться внутри тега <SQL>.

 

  <VMs> – И самое интересное, описание виртуальных машин.
    <Count>3</Count> – Количество машин.
    <Domain> – Создаем домен. Все OU указанные ниже будут созданы (если их уже нет), как и OU указанная в разделе JoinDomain. Все пользователи и группы указанные в файле Variable.xml будут созданы в домене и "сложены" в указанные ниже OU.
      <Name>contoso.com</Name> – Имя домена.
      <ServiceAccountOU>Users</ServiceAccountOU> – Имя контейнера для пользователей.
      <GroupOU>Groups</GroupOU> – Имя контейнера для групп.
    </Domain>
    <Default> – Общая для всех виртуальных машин секция.
      <Host>Localhost</Host> – Hyper-V хост, на котором необходимо создать виртуальные машины.
      <VMFolder>C:VMs</VMFolder> – Путь по которому будет создана папка виртуальной машины и её файлы конфигурации.
      <VHDFolder>C:VMs</VHDFolder> – Путь по которому будет создана папка виртуальной машины и её жесткие диски.
      <VMName> – Секция для автоматического наименования виртуальных машин, я так и не понял что она делает, ни при каких обстоятельствах у меня она не работала. Есть подозрение что она используется если не давать виртуальным машинам имена, но это крайне не удобно.
        <Prefix>WS12R2D</Prefix>
        <Sequence>1</Sequence>
      </VMName>
      <Processor>2</Processor> –  Процессор.
      <Memory> – Память.
        <Startup>1024</Startup>
        <Minimum>512</Minimum>
        <Maximum>2048</Maximum>
        <Buffer>20</Buffer>
      </Memory>
      <NetworkAdapter> – Сетевой адаптер.
        <VirtualSwitch>dflt</VirtualSwitch> – Необходимо указать точное имя виртуального адаптера, который необходимо использовать при создании виртуальных машин.
        <MAC>
          <Prefix>00:15:5D:65:01:</Prefix>
          <Sequence>4</Sequence>
        </MAC>
        <IP>
          <Prefix>192.168.1.</Prefix> – В IP адресе и в MAC адресе используется один и тот же принцип, Вы задаете начальное значение и сдвиг. В данном случае первая виртуальная машина получит MAC 00155D540104 и IP 192.168.1.4.
          <Sequence>4</Sequence>
          <Mask>24</Mask>
          <Gateway>192.168.1.4</Gateway>
          <DNS>192.168.1.4</DNS> – Здесь указан адрес 192.168.1.4, так как это адрес первой виртуальной машины, и она будет домен контроллером.
        </IP>
      </NetworkAdapter>
      <OSDisk> – Диск с операционной системой.
        <Parent>C:Installergen2.vhdx</Parent> – Исходный диск.
        <Type>Differencing</Type> – Каким образом создавать новый диск ("Copy" или "Differencing").
      </OSDisk>
      <DataDisks> – Диски с данными, создаются пустыми.
        <Count>1</Count>
        <Format>VHDX</Format>
        <Size>100</Size>
      </DataDisks>
      <DVD>False</DVD>
      <AutoStart>
        <Action>Nothing</Action>
        <Delay>0</Delay>
      </AutoStart>
      <JoinDomain> – Вводим виртуальную машину в домен.
        <Domain>contoso.com</Domain>
        <Credentials>
          <Domain>contoso.com</Domain>
          <Password>!Q2w3e4r</Password>
          <Username>!jd</Username>
        </Credentials>
        <OrganizationalUnit>Servers.HQ</OrganizationalUnit> – OU, в которую будет введена виртуальная машина. В данном случае в корне домена будет создан контейнер HQ, а в нем контейнер Servers, куда будут добавлены все виртуальные машины.
      </JoinDomain>
      <AdministratorPassword>!Q2w3e4r</AdministratorPassword> – Пароль локального администратора.
      <VMGeneration>2</VMGeneration> – Поколение машины. 
      <GuestServices>True</GuestServices> – Гостевые сервисы.
    </Default>
    <VM Count="1">
      <VMName>DC-01</VMName>
      <DataDisks> – На данных дисках будут расположены файлы AD DS.
        <Count>2</Count>
        <Format>VHDX</Format>
        <Size>100</Size>
      </DataDisks>
    </VM>
    <VM Count="2">
      <VMName>SQL-01</VMName>
      <Memory>
        <Startup>1024</Startup>
        <Minimum>512</Minimum>
        <Maximum>8192</Maximum>
        <Buffer>5</Buffer>
      </Memory>
      <DataDisks>
        <Count>3</Count>
        <Format>VHDX</Format>
        <Size>100</Size>
      </DataDisks>
    </VM>
    <VM Count="3">
      <VMName>VMM-01</VMName>
      <Memory> – VMM требует 2гб оперативной памяти, не забываем про это.
        <Startup>2048</Startup>
        <Minimum>2048</Minimum>
        <Maximum>2048</Maximum>
        <Buffer>20</Buffer>
      </Memory>
  </VMs>
</Installer>
```

О моих мытарствах с данным файлом я расскажу в <a href="http://4c74356b41.com/post593">следующей статье</a>.