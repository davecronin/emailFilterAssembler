# Email Filter Assembler

A small assembler that turns language specifying email filers into XML that can be read Gmail
or any other email hosts that use the same standard for specifying filters. 
This language provides a simpler way of writing and managing these filters than the 
Gmail interface since the information is more compact and understandable with 
large numbers of filters, elements can be reused, and nested filters can be created to 
allow more specific behaviour without duplication.


## Prerequisites

You just need Python installed (tested 2.6, 2.7, 3.3, 3.4, 3.5, 3.6)

## Getting Started

The input must follow some rules or syntax like any language to be parsed correctly.

### Matchers

Matchers are the part of the filter that determine what emails the filter will apply to.
The are specified between curly braces. eg { matcher content }

The content is in the form <attribute> "<pattern>"

For example:
``` 
{to "my_email@example.com"}
```
The following attributes can be specified:
* to
* from
* subject
* contains
* notContains

The pattern will then be formatted for XML (escaped correctly) and assigned to that
attribute.

Multiple attributes can be specified, separated by commas, eg,
```
{to "my_email@example.com", subject "Birthday plans"}
```

### Actions

Actions are the part of the filter that determine what the filter will do to emails 
that the filter applies to.
The are specified between square braces. eg [ matcher content ]

The content is in the form of comma separated key words or phrases.

For example:
``` 
[mark as read, archive]
```
The following actions can be specified:
* mark as read | mark read | read
* star
* delete | bin | trash
* archive
* not spam | never spam
* mark as important | mark important | important

There is an additional action with a different format:
* label "labelToBeApplied"
Nested labels can be specified, ie "someTopic/subLabel", however unless the label already
exists in Gmail then it wont be created when the XML is imported. Please create the nested
labels you want before importing the XML.

### Variables

In order to reuse these combinations of Matchers or Actions you can create variables :
```
birthdayEmails = {to "my_email@example.com", contains "birthday"}
```
Variables are only available after the point in the file they were declared.

### Statements

Statements are used to actually specify the filters you want to create. 
They can declare matchers and actions inline or use variables are in the form:
```
if {from "spam@spam.com"} -> [delete, mark read]

birthdayEmails = {to "my_email@example.com", contains "birthday"}

if birthdayEmails -> [mark important, star]
```
This will create two filters in the XML output file with the desired actions.

Nested statements can also be specified to have greater control over similar filters
with different actions. For example:
```
invoices = {subject "invoice|bill"}

if invoices -> [archive, read, label "Invoices"]
	if {from "cabelProvider"} -> [label "Invoices/CableCompany"]
	if {from "electricity"} -> [label "Invoices/Electricity"]
```
This will create three filters: the parent filter, and the two indented ones will combine 
their matchers with their parents, and will use their parents actions unless they 
supply one, in which case the child's action will override the parent.

These can be quite powerful if, for example, you get a lot of email from a mailing list
and want to filter out certain topics, emails that mention your name, or any other criteria, 
without having to specify the same things repeatedly for each filter. 

### Syntax specifics
* All variables and statements must be declared in a single line. (There is an issue open
to fix this)
* Variables must have no leading indentation or whitespace.
* Nested or indented statements must be indented with tabs, not spaces. (Will also be fixed) 

## Running this program

Just download this code and call main.py with the input and output files specified, where
the input file contains your filters you want, and the output will contain the resulting
XML.

```
emailFilterAssembler/main.py my_input.txt my_output.xml
```

To upload it to Gmail, go to 
* Settings>Filters and blocked addresses
* Select "Import filters"
* Select the output XML file
* Click "Open file"
* Tick the filters you want to create
* To apply to existing emails tick the box for "Apply new filters to existing email."
* Click "Create filters"

! Remember nested labels can be specified, ie "someTopic/subLabel", however 
unless the label already exists in Gmail then it wont be created when the XML 
is imported. Please create the nested labels you want before importing the XML.