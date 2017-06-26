---
id: 767
title: 'VM Authoring Tool - Новая роль виртуальной машины'
date: 2014-06-25T16:25:49+00:00
author: rootilo
layout: post
guid: http://4c74356b41.com/post767
permalink: /post767
categories:
  - Azure Pack
  - Virtualization and Cloud
tags:
  - Guide
  - Virtual Machine Manager
  - VM Authoring Tool
  - Windows Azure Pack
---
Приступим к изучению VM Authoring Tool.  
  
VM Authoring Tool представляет из себя утилиту для создания и редактирования Resource Definition и Extension файлов.
  
Предлагаю Вам просмотреть 2 видео от Charles Joy сотрудника Microsoft.
  
<a href="http://youtu.be/iCilD2P8vhE" target="_blank">VM Role Resource Extension</a> и <a href="http://youtu.be/66zznivfh_s" target="_blank">VM Role Resource Definition</a>

**Приступим к работе с VM Authoring Tool**

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_New_Package.png" rel="attachment wp-att-4968"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_New_Package-300x135.png" alt="VM_Auth_New_Package" width="300" height="135" /></a>
  
Вначале Вам необходимо создать новые Resource Definition и Extension пакеты. Задать им название и путь где они будут расположены;

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Package_Overview.png" rel="attachment wp-att-4971"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Package_Overview-265x300.png" alt="VM_Auth_Package_Overview" width="265" height="300" /></a>
  
После того как Вы создали эти файлы, они будут автоматически открыты в утилите. Теперь можно начинать менять настройки;
  
<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_VHD_Tag.png" rel="attachment wp-att-4978"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_VHD_Tag-300x38.png" alt="VM_Auth_VHD_Tag" width="300" height="38" /></a>
  
Для начала необходимо изменить тэг для жесткого диска с операционной системой, можно указать несколько тэгов. Данные тэги необходимо будет [присвоить диску](http://4c74356b41.com/post757);

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Roles_Features.png" rel="attachment wp-att-4974"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Roles_Features-300x44.png" alt="VM_Auth_Roles_Features" width="300" height="44" /></a>
  
Если Вам необходимо настроить роли или компоненты операционной системы воспользуйтесь пунктом "Roles and Features"

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_App_Customization.png" rel="attachment wp-att-4941"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_App_Customization-300x205.png" alt="VM_Auth_App_Customization" width="300" height="205" /></a>
  
Если Вы хотите добавить кастомные приложения в виртуальную машину, Вы можете воспользоваться меню "Add" и добавить соответствующие скрипты, приложения, профили sql и так далее, по аналогии с VMM. В Data Package необходимо указать путь к пакету. В качестве значения по умолчанию указано "src". Это значит что при импорте в VMM в папке где находится Resource Extension должна находится папка src и в ней папки и файлы, которые надо будет указать. Все пути к файлам необходимо указывать относительно папки src.

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Bind_Definition.png" rel="attachment wp-att-4944"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Bind_Definition-300x109.png" alt="VM_Auth_Bind_Definition" width="300" height="109" /></a>
  
Для того чтобы связать данные пакеты Вам необходимо указать в Extension References пакета Resource Definition использовать пакет Resource Extension;

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Join_Domain.png" rel="attachment wp-att-4958"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Join_Domain-300x127.png" alt="VM_Auth_Join_Domain" width="300" height="127" /></a>
  
Если Вы хотите, чтобы компьютер автоматически добавлялся в домен, Вам необходимо в пункте "Operating System Profile" выбрать пункт "JoinDomain" и сгенерировать 2 новых переменных (выбрав в выпадающем меню пункт "Generate new parameter") для полей "DomainToJoin" и "DomainJoinCredentials"
  
DomainJoinCredentials при заполнении формы на портале необходимо указывать в формате domainuser

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Generated_Parameters.png" rel="attachment wp-att-4953"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Generated_Parameters-300x83.png" alt="VM_Auth_Generated_Parameters" width="300" height="83" /></a>
  
После этого Вы можете убедиться, что в пакет добавилось 2 новых переменных (тип присвоился автоматически, но вы можете его изменить);

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Check_Tag.png" rel="attachment wp-att-4948"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Check_Tag-300x130.png" alt="VM_Auth_Check_Tag" width="300" height="130" /></a>
  
В пункте View Definition Вы можете настроить поля, которые необходимо будет заполнить пользователю. Обратите внимание что поле тэг диска было заполнено автоматически. При необходимости можно разделить мастер создания роли виртуальной машины на несколько страниц (по умолчанию одна). Для этого необходимо добавить View Definition Section. Поле Name будет отображено пользователю при запросе данных;

<a href="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Network_and_Validate.png" rel="attachment wp-att-4963"><img src="http://4c74356b41.com/wp-content/uploads/2016/02/VM_Auth_Network_and_Validate-300x248.png" alt="VM_Auth_Network_and_Validate" width="300" height="248" /></a>
  
Кроме всего прочего, в пункте Network Profile можно настроить сеть. 😉
  
Закончить процесс создания пакетов, желательно, валидацией.

Для импортирования пакетов в VMM и WAP необходимо использовать [уже описанную мной](http://4c74356b41.com/post757) процедуру.