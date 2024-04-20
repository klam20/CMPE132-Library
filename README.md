# CMPE132-Library

ABAC (attribute-based access control) is a newer approach to access control in comparison to
the RBAC (role-based access control). The main concept of the ABAC is the utilization of
attributes on the subjects, objects, and environment to create a policy-driven system on granting
and denying access

There are most definitely criteria and decision processes involved in selecting an ABAC system
over other systems.

One advantage of choosing an ABAC is the granularity of control you get in providing or denying
access. In comparison to an RBAC or MAC (mandatory access control) the ABAC does not rely
on specific levels or roles of clearance in providing access. Instead ABAC considers multiple
various attributes of the subject, object, and environment to determine if access should be
granted. For example to see the granularity of control one can imagine that a user accessing the
library has many other attributes that define them such as if they are a student, what major, year
of study, graduate or not, etc...Such factors introduce many complex nested layers in an RBAC,
or additional separate student roles, but are instead just attributes for a simple student structure
in an ABAC.

Another major point of using an ABAC for either good or bad, is that there is less burden on the
implementation of subjects and objects since it is easy to add attributes rather than more roles,
but this subsequently means the burden falls on the control policy that dictates how access is
given which is sure to increase in complexity.
The last point to highlight is that a unique environment variable is factored into a ABAC system.
This variable considers things like location or time meaning access can be controlled due to
dynamic factors such as when someone made a request or from what country they made that
request in. This feature offers greater security in comparison to access control schemes that do
not employ environmental factors

I will be implementing the ABAC using a popular library called py_abac
There is documentation available at https://py-abac.readthedocs.io/en/latest/ and at a high level
allows for defining policies in JSON-like format, managing the policies with add/remove/update
operations, and providing APIs that have runtime control decision-making.

Run using 
> python3 run.py