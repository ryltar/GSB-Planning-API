------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------



------------------------------------------------------------
-- Table: address
------------------------------------------------------------
CREATE TABLE public.address(
	id         SERIAL NOT NULL ,
	num        VARCHAR (10) NOT NULL ,
	street     VARCHAR (255) NOT NULL ,
	codepost   VARCHAR (10) NOT NULL ,
	city       VARCHAR (255) NOT NULL ,
	country    VARCHAR (255) NOT NULL ,
	indication VARCHAR (255) NOT NULL ,
	CONSTRAINT prk_constraint_address PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: appointment
------------------------------------------------------------
CREATE TABLE public.appointment(
	id         SERIAL NOT NULL ,
	start_date DATE  NOT NULL ,
	end_date   DATE  NOT NULL ,
	state      INT  NOT NULL ,
	feedback   VARCHAR (2000)   ,
	id_doctor  INT  NOT NULL ,
	CONSTRAINT prk_constraint_appointment PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: doctor
------------------------------------------------------------
CREATE TABLE public.doctor(
	id           SERIAL NOT NULL ,
	lastname     VARCHAR (80) NOT NULL ,
	firstname    VARCHAR (80) NOT NULL ,
	num_tel      VARCHAR (25) NOT NULL ,
	email        VARCHAR (25) NOT NULL ,
	id_specialty INT  NOT NULL ,
	id_address   INT  NOT NULL ,
	id_employee  INT  NOT NULL ,
	CONSTRAINT prk_constraint_doctor PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: employee
------------------------------------------------------------
CREATE TABLE public.employee(
	id        SERIAL NOT NULL ,
	lastname  VARCHAR (80) NOT NULL ,
	firstname VARCHAR (80) NOT NULL ,
	is_admin  BOOL   ,
	passwd    VARCHAR (80) NOT NULL ,
	email     VARCHAR (255) NOT NULL UNIQUE,
	num_tel   VARCHAR (25) NOT NULL ,
	pseudo    VARCHAR (255) NOT NULL UNIQUE,
	CONSTRAINT prk_constraint_employee PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: medic
------------------------------------------------------------
CREATE TABLE public.medic(
	id          SERIAL NOT NULL ,
	lib         VARCHAR (80) NOT NULL UNIQUE,
	description VARCHAR (2000) NOT NULL ,
	CONSTRAINT prk_constraint_medic PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: specialty
------------------------------------------------------------
CREATE TABLE public.specialty(
	id    SERIAL NOT NULL ,
	label VARCHAR (80) NOT NULL ,
	CONSTRAINT prk_constraint_specialty PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: maintenance
------------------------------------------------------------
CREATE TABLE public.maintenance(
	id             SERIAL NOT NULL ,
	in_maintenance BOOL   ,
	CONSTRAINT prk_constraint_maintenance PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: is_mentioned
------------------------------------------------------------
CREATE TABLE public.is_mentioned(
	id             INT  NOT NULL ,
	id_appointment INT  NOT NULL ,
	CONSTRAINT prk_constraint_is_mentioned PRIMARY KEY (id,id_appointment)
)WITHOUT OIDS;



ALTER TABLE public.appointment ADD CONSTRAINT FK_appointment_id_doctor FOREIGN KEY (id_doctor) REFERENCES public.doctor(id);
ALTER TABLE public.doctor ADD CONSTRAINT FK_doctor_id_specialty FOREIGN KEY (id_specialty) REFERENCES public.specialty(id);
ALTER TABLE public.doctor ADD CONSTRAINT FK_doctor_id_address FOREIGN KEY (id_address) REFERENCES public.address(id);
ALTER TABLE public.doctor ADD CONSTRAINT FK_doctor_id_employee FOREIGN KEY (id_employee) REFERENCES public.employee(id);
ALTER TABLE public.is_mentioned ADD CONSTRAINT FK_is_mentioned_id FOREIGN KEY (id) REFERENCES public.medic(id);
ALTER TABLE public.is_mentioned ADD CONSTRAINT FK_is_mentioned_id_appointment FOREIGN KEY (id_appointment) REFERENCES public.appointment(id);
