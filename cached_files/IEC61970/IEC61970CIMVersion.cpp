///////////////////////////////////////////////////////////
//  IEC61970CIMVersion.cpp
//  Implementation of the Class IEC61970CIMVersion
///////////////////////////////////////////////////////////

#include "IEC61970CIMVersion.h"

using IEC61970CIMVersion;

IEC61970CIMVersion::IEC61970CIMVersion(){}

IEC61970CIMVersion::~IEC61970CIMVersion(){}

const Date IEC61970CIMVersion::date = IEC61970::Base::Domain::Date("2017-07-26");
const String IEC61970CIMVersion::version = "IEC61970CIM17v23";
