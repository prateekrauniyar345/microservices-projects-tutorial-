# Microservices

**What is Microservices ?**\
Microservices is an architectural style that structures an application as a collection of small, autonomous services modeled around a business domain. Each service is self-contained, independently deployable, and responsible for a specific functionality.



**Monolithic vs. Microservices Architecture**\
With monolithic architectures, all processes are tightly coupled and run as a single service. This means that if one process of the application experiences a spike in demand, the entire architecture must be scaled. Adding or improving a monolithic application’s features becomes more complex as the code base grows. This complexity limits experimentation and makes it difficult to implement new ideas. Monolithic architectures add risk for application availability because many dependent and tightly coupled processes increase the impact of a single process failure.

![Monolith V/S Microservices](./doc%20assets/monolith%20vs%20microservices.png)

With a microservices architecture, an application is built as independent components that run each application process as a service. These services communicate via a well-defined interface using lightweight APIs. Services are built for business capabilities and each service performs a single function. Because they are independently run, each service can be updated, deployed, and scaled to meet demand for specific functions of an application.


