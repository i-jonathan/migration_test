CREATE TABLE Adjudicator (
    AdjudicatorId INT PRIMARY KEY,
    Surname VARCHAR(255),
    Forenames VARCHAR(255),
    Title VARCHAR(50),
    DateOfBirth DATE,
    CorrespondenceAddress VARCHAR(255),
    ContactTelephone VARCHAR(50),
    ContactDetails TEXT,
    AvailableAtShortNotice BOOLEAN,
    CentreId INT,  -- Foreign key to HearingCentre table
    EmploymentTermId INT,  -- Foreign key to EmploymentTerm table
    FullTime BOOLEAN,
    IdentityNumber VARCHAR(50),
    DateOfRetirement DATE,
    ContractEndDate DATE,
    ContractRenewalDate DATE,
    DoNotUseReasonId INT,  -- Foreign key to DoNotUseReason table
    JudicialStatus VARCHAR(255),
    Address1 VARCHAR(255),
    Address2 VARCHAR(255),
    Address3 VARCHAR(255),
    Address4 VARCHAR(255),
    Address5 VARCHAR(255),
    Postcode VARCHAR(20),
    Telephone VARCHAR(50),
    Mobile VARCHAR(50),
    Email VARCHAR(255),
    BusinessAddress1 VARCHAR(255),
    BusinessAddress2 VARCHAR(255),
    BusinessAddress3 VARCHAR(255),
    BusinessAddress4 VARCHAR(255),
    BusinessAddress5 VARCHAR(255),
    BusinessPostcode VARCHAR(20),
    BusinessTelephone VARCHAR(50),
    BusinessFax VARCHAR(50),
    BusinessEmail VARCHAR(255),
    JudicialInstructions TEXT,
    JudicialInstructionsDate DATE,
    Notes TEXT
);

CREATE TABLE JOHistory (
    AdjudicatorId INT,  -- Foreign key to Adjudicator table
    HistDate DATE,
    HistType VARCHAR(255),
    UserId INT,  -- Foreign key to Users table
    Comment TEXT,
    FOREIGN KEY (AdjudicatorId) REFERENCES Adjudicator(AdjudicatorId)
);

CREATE TABLE OtherCentre (
    AdjudicatorId INT,  -- Foreign key to Adjudicator table
    CentreId INT,  -- Foreign key to HearingCentre table
    FOREIGN KEY (AdjudicatorId) REFERENCES Adjudicator(AdjudicatorId)
);

CREATE TABLE AdjudicatorRole (
    AdjudicatorId INT,  -- Foreign key to Adjudicator table
    Role VARCHAR(255),
    DateOfAppointment DATE,
    EndDateOfAppointment DATE,
    FOREIGN KEY (AdjudicatorId) REFERENCES Adjudicator(AdjudicatorId)
);

CREATE TABLE HearingCentre (
    CentreId INT PRIMARY KEY,
    Description VARCHAR(255)
);

CREATE TABLE EmploymentTerm (
    EmploymentTermId INT PRIMARY KEY,
    Description VARCHAR(255)
);

CREATE TABLE DoNotUseReason (
    DoNotUseReasonId INT PRIMARY KEY,
    Description VARCHAR(255)
);

CREATE TABLE Users (
    UserId INT PRIMARY KEY,
    FullName VARCHAR(255)
);
