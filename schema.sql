CREATE TYPE "InvoiceStatus" AS ENUM ('DRAFT', 'SENT', 'PAID', 'OVERDUE', 'CANCELLED')
CREATE TYPE "HaciendaStatus" AS ENUM ('PENDING', 'SUBMITTED', 'APPROVED', 'REJECTED')
CREATE TYPE "UserType" AS ENUM ('SHIPPER', 'CARRIER', 'ADMIN')
CREATE TYPE "UserStatus" AS ENUM ('PENDING', 'ACTIVE', 'SUSPENDED', 'BANNED')
CREATE TYPE "KYCStatus" AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'EXPIRED')
CREATE TYPE "PaymentType" AS ENUM ('SHIPMENT', 'INSURANCE', 'FEE', 'REFUND')
CREATE TYPE "PaymentMethod" AS ENUM ('CREDIT_CARD', 'DEBIT_CARD', 'BANK_TRANSFER', 'SINPE_MOVIL', 'CASH')
CREATE TYPE "PaymentStatus" AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'CANCELLED', 'REFUNDED')
CREATE TYPE "Priority" AS ENUM ('LOW', 'NORMAL', 'HIGH', 'URGENT')
CREATE TYPE "ServiceLevel" AS ENUM ('ECONOMY', 'STANDARD', 'EXPRESS')
CREATE TYPE "ShipmentStatus" AS ENUM ('PENDING', 'ACCEPTED', 'PICKUP_SCHEDULED', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED')
CREATE TYPE "BusinessType" AS ENUM ('INDIVIDUAL', 'COMPANY')
CREATE TYPE "TrackingEvent" AS ENUM ('CREATED', 'ACCEPTED', 'PICKUP_SCHEDULED', 'EN_ROUTE_PICKUP', 'ARRIVED_PICKUP', 'LOADED', 'IN_TRANSIT', 'ARRIVED_DELIVERY', 'DELIVERED', 'EXCEPTION')
CREATE TYPE "VehicleType" AS ENUM ('PICKUP', 'VAN', 'TRUCK', 'TRAILER')
CREATE TYPE "FuelType" AS ENUM ('GASOLINE', 'DIESEL', 'ELECTRIC', 'HYBRID')

CREATE TABLE users (
	id TEXT NOT NULL, 
	email TEXT NOT NULL, 
	"emailVerified" TIMESTAMP WITHOUT TIME ZONE, 
	"passwordHash" TEXT NOT NULL, 
	"userType" "UserType" DEFAULT 'SHIPPER'::"UserType" NOT NULL, 
	status "UserStatus" DEFAULT 'PENDING'::"UserStatus" NOT NULL, 
	"firstName" TEXT NOT NULL, 
	"lastName" TEXT NOT NULL, 
	phone TEXT NOT NULL, 
	"nationalId" TEXT, 
	"companyName" TEXT, 
	"companyRegistration" TEXT, 
	"taxId" TEXT, 
	"addressLine1" TEXT, 
	"addressLine2" TEXT, 
	city TEXT, 
	province TEXT, 
	"postalCode" TEXT, 
	country TEXT DEFAULT 'CR'::text NOT NULL, 
	language TEXT DEFAULT 'es'::text NOT NULL, 
	currency TEXT DEFAULT 'CRC'::text NOT NULL, 
	timezone TEXT DEFAULT 'America/Costa_Rica'::text NOT NULL, 
	"emailVerifiedAt" TIMESTAMP WITHOUT TIME ZONE, 
	"phoneVerifiedAt" TIMESTAMP WITHOUT TIME ZONE, 
	"kycStatus" "KYCStatus" DEFAULT 'PENDING'::"KYCStatus" NOT NULL, 
	"kycVerifiedAt" TIMESTAMP WITHOUT TIME ZONE, 
	"dataConsent" BOOLEAN DEFAULT false NOT NULL, 
	"dataConsentDate" TIMESTAMP WITHOUT TIME ZONE, 
	"marketingConsent" BOOLEAN DEFAULT false NOT NULL, 
	"createdAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"updatedAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"deletedAt" TIMESTAMP WITHOUT TIME ZONE, 
	CONSTRAINT users_pkey PRIMARY KEY (id), 
	CONSTRAINT users_email_unique UNIQUE NULLS DISTINCT (email)
)



CREATE TABLE shipments (
	id TEXT NOT NULL, 
	"shipmentNumber" TEXT NOT NULL, 
	"trackingNumber" TEXT NOT NULL, 
	"shipperId" TEXT NOT NULL, 
	"carrierId" TEXT, 
	description TEXT NOT NULL, 
	"cargoType" TEXT NOT NULL, 
	"pickupContactName" TEXT NOT NULL, 
	"pickupContactPhone" TEXT NOT NULL, 
	"pickupAddressLine1" TEXT NOT NULL, 
	"pickupAddressLine2" TEXT, 
	"pickupProvince" TEXT NOT NULL, 
	"pickupCity" TEXT NOT NULL, 
	"pickupDate" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"pickupTimeStart" TEXT, 
	"pickupTimeEnd" TEXT, 
	"pickupInstructions" TEXT, 
	"deliveryContactName" TEXT NOT NULL, 
	"deliveryContactPhone" TEXT NOT NULL, 
	"deliveryAddressLine1" TEXT NOT NULL, 
	"deliveryAddressLine2" TEXT, 
	"deliveryProvince" TEXT NOT NULL, 
	"deliveryCity" TEXT NOT NULL, 
	"deliveryDateRequested" TIMESTAMP WITHOUT TIME ZONE, 
	"deliveryInstructions" TEXT, 
	"weightKg" DOUBLE PRECISION NOT NULL, 
	"lengthCm" DOUBLE PRECISION, 
	"widthCm" DOUBLE PRECISION, 
	"heightCm" DOUBLE PRECISION, 
	"valueAmount" DOUBLE PRECISION, 
	"isFragile" BOOLEAN DEFAULT false NOT NULL, 
	"requiresRefrigeration" BOOLEAN DEFAULT false NOT NULL, 
	"requiresInsurance" BOOLEAN DEFAULT false NOT NULL, 
	priority "Priority" DEFAULT 'NORMAL'::"Priority" NOT NULL, 
	"serviceLevel" "ServiceLevel" DEFAULT 'STANDARD'::"ServiceLevel" NOT NULL, 
	"specialInstructions" TEXT, 
	"requiresPackaging" BOOLEAN DEFAULT false NOT NULL, 
	"requiresAssembly" BOOLEAN DEFAULT false NOT NULL, 
	"requiresAppointment" BOOLEAN DEFAULT false NOT NULL, 
	"quotedAmount" DOUBLE PRECISION NOT NULL, 
	currency TEXT DEFAULT 'CRC'::text NOT NULL, 
	status "ShipmentStatus" DEFAULT 'PENDING'::"ShipmentStatus" NOT NULL, 
	"currentLocation" TEXT, 
	"estimatedDelivery" TIMESTAMP WITHOUT TIME ZONE, 
	"actualPickupTime" TIMESTAMP WITHOUT TIME ZONE, 
	"actualDeliveryTime" TIMESTAMP WITHOUT TIME ZONE, 
	"createdAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"updatedAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"deletedAt" TIMESTAMP WITHOUT TIME ZONE, 
	CONSTRAINT shipments_pkey PRIMARY KEY (id), 
	CONSTRAINT "shipments_shipmentNumber_unique" UNIQUE NULLS DISTINCT ("shipmentNumber"), 
	CONSTRAINT "shipments_trackingNumber_unique" UNIQUE NULLS DISTINCT ("trackingNumber")
)



CREATE TABLE carriers (
	id TEXT NOT NULL, 
	"userId" TEXT NOT NULL, 
	"businessType" "BusinessType" DEFAULT 'INDIVIDUAL'::"BusinessType" NOT NULL, 
	"serviceAreas" TEXT[], 
	specializations TEXT[], 
	"maxWeightKg" INTEGER, 
	"maxVolumeM3" DOUBLE PRECISION, 
	"vehicleCount" INTEGER DEFAULT 0 NOT NULL, 
	rating DOUBLE PRECISION DEFAULT 0.0 NOT NULL, 
	"totalRatings" INTEGER DEFAULT 0 NOT NULL, 
	"completedShipments" INTEGER DEFAULT 0 NOT NULL, 
	"onTimePercentage" DOUBLE PRECISION DEFAULT 0.0 NOT NULL, 
	"paymentMethod" "PaymentMethod" DEFAULT 'BANK_TRANSFER'::"PaymentMethod" NOT NULL, 
	"bankAccountNumber" TEXT, 
	"bankName" TEXT, 
	"sinpeMovilNumber" TEXT, 
	"isAvailable" BOOLEAN DEFAULT true NOT NULL, 
	"availabilitySchedule" JSONB, 
	"createdAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"updatedAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"deletedAt" TIMESTAMP WITHOUT TIME ZONE, 
	CONSTRAINT carriers_pkey PRIMARY KEY (id), 
	CONSTRAINT "carriers_userId_unique" UNIQUE NULLS DISTINCT ("userId")
)



CREATE TABLE "Session" (
	id TEXT NOT NULL, 
	"sessionToken" TEXT NOT NULL, 
	"userId" TEXT NOT NULL, 
	expires TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	CONSTRAINT "Session_pkey" PRIMARY KEY (id), 
	CONSTRAINT "Session_sessionToken_unique" UNIQUE NULLS DISTINCT ("sessionToken")
)



CREATE TABLE "Account" (
	id TEXT NOT NULL, 
	"userId" TEXT NOT NULL, 
	type TEXT NOT NULL, 
	provider TEXT NOT NULL, 
	"providerAccountId" TEXT NOT NULL, 
	refresh_token TEXT, 
	access_token TEXT, 
	expires_at INTEGER, 
	token_type TEXT, 
	scope TEXT, 
	id_token TEXT, 
	session_state TEXT, 
	CONSTRAINT "Account_pkey" PRIMARY KEY (id), 
	CONSTRAINT "Account_provider_providerAccountId_unique" UNIQUE NULLS DISTINCT (provider, "providerAccountId")
)



CREATE TABLE cargo_types (
	id TEXT NOT NULL, 
	name TEXT NOT NULL, 
	description TEXT, 
	"baseRateMultiplier" DOUBLE PRECISION DEFAULT 1 NOT NULL, 
	"insuranceRequired" BOOLEAN DEFAULT false NOT NULL, 
	"minimumInsuranceAmount" DOUBLE PRECISION, 
	"requiresSpecialHandling" BOOLEAN DEFAULT false NOT NULL, 
	"requiresSpecialEquipment" BOOLEAN DEFAULT false NOT NULL, 
	"equipmentRequirements" TEXT[], 
	"cabysCode" TEXT, 
	"taxRate" DOUBLE PRECISION DEFAULT 13 NOT NULL, 
	"isActive" BOOLEAN DEFAULT true NOT NULL, 
	"createdAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"updatedAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	CONSTRAINT cargo_types_pkey PRIMARY KEY (id), 
	CONSTRAINT cargo_types_name_unique UNIQUE NULLS DISTINCT (name)
)



CREATE TABLE pg_stat_statements_info (
	dealloc BIGINT, 
	stats_reset TIMESTAMP WITH TIME ZONE
)



CREATE TABLE pg_stat_statements (
	userid OID, 
	dbid OID, 
	toplevel BOOLEAN, 
	queryid BIGINT, 
	query TEXT, 
	plans BIGINT, 
	total_plan_time DOUBLE PRECISION, 
	min_plan_time DOUBLE PRECISION, 
	max_plan_time DOUBLE PRECISION, 
	mean_plan_time DOUBLE PRECISION, 
	stddev_plan_time DOUBLE PRECISION, 
	calls BIGINT, 
	total_exec_time DOUBLE PRECISION, 
	min_exec_time DOUBLE PRECISION, 
	max_exec_time DOUBLE PRECISION, 
	mean_exec_time DOUBLE PRECISION, 
	stddev_exec_time DOUBLE PRECISION, 
	rows BIGINT, 
	shared_blks_hit BIGINT, 
	shared_blks_read BIGINT, 
	shared_blks_dirtied BIGINT, 
	shared_blks_written BIGINT, 
	local_blks_hit BIGINT, 
	local_blks_read BIGINT, 
	local_blks_dirtied BIGINT, 
	local_blks_written BIGINT, 
	temp_blks_read BIGINT, 
	temp_blks_written BIGINT, 
	shared_blk_read_time DOUBLE PRECISION, 
	shared_blk_write_time DOUBLE PRECISION, 
	local_blk_read_time DOUBLE PRECISION, 
	local_blk_write_time DOUBLE PRECISION, 
	temp_blk_read_time DOUBLE PRECISION, 
	temp_blk_write_time DOUBLE PRECISION, 
	wal_records BIGINT, 
	wal_fpi BIGINT, 
	wal_bytes NUMERIC, 
	jit_functions BIGINT, 
	jit_generation_time DOUBLE PRECISION, 
	jit_inlining_count BIGINT, 
	jit_inlining_time DOUBLE PRECISION, 
	jit_optimization_count BIGINT, 
	jit_optimization_time DOUBLE PRECISION, 
	jit_emission_count BIGINT, 
	jit_emission_time DOUBLE PRECISION, 
	jit_deform_count BIGINT, 
	jit_deform_time DOUBLE PRECISION, 
	stats_since TIMESTAMP WITH TIME ZONE, 
	minmax_stats_since TIMESTAMP WITH TIME ZONE
)



CREATE TABLE payments (
	id TEXT NOT NULL, 
	"paymentNumber" TEXT NOT NULL, 
	"shipmentId" TEXT NOT NULL, 
	"payerId" TEXT NOT NULL, 
	"payeeId" TEXT NOT NULL, 
	amount DOUBLE PRECISION NOT NULL, 
	currency TEXT DEFAULT 'CRC'::text NOT NULL, 
	"paymentType" "PaymentType" NOT NULL, 
	"paymentMethod" "PaymentMethod" NOT NULL, 
	status "PaymentStatus" DEFAULT 'PENDING'::"PaymentStatus" NOT NULL, 
	"externalTransactionId" TEXT, 
	"gatewayResponse" TEXT, 
	"dueDate" DATE, 
	"processedAt" TIMESTAMP WITHOUT TIME ZONE, 
	"completedAt" TIMESTAMP WITHOUT TIME ZONE, 
	"invoiceXml" TEXT, 
	"invoiceKey" TEXT, 
	"haciendaStatus" "HaciendaStatus" DEFAULT 'PENDING'::"HaciendaStatus", 
	"haciendaResponse" TEXT, 
	"createdAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"updatedAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"createdBy" TEXT, 
	CONSTRAINT payments_pkey PRIMARY KEY (id), 
	CONSTRAINT "payments_createdBy_users_id_fk" FOREIGN KEY("createdBy") REFERENCES users (id), 
	CONSTRAINT "payments_payeeId_users_id_fk" FOREIGN KEY("payeeId") REFERENCES users (id), 
	CONSTRAINT "payments_payerId_users_id_fk" FOREIGN KEY("payerId") REFERENCES users (id), 
	CONSTRAINT "payments_shipmentId_shipments_id_fk" FOREIGN KEY("shipmentId") REFERENCES shipments (id), 
	CONSTRAINT "payments_paymentNumber_unique" UNIQUE NULLS DISTINCT ("paymentNumber")
)



CREATE TABLE "trackingEvents" (
	id TEXT NOT NULL, 
	"shipmentId" TEXT NOT NULL, 
	"eventType" "TrackingEvent" NOT NULL, 
	description TEXT NOT NULL, 
	notes TEXT, 
	latitude DOUBLE PRECISION, 
	longitude DOUBLE PRECISION, 
	address TEXT, 
	"eventTimestamp" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"createdBy" TEXT, 
	"isAutomatic" BOOLEAN DEFAULT false NOT NULL, 
	metadata TEXT, 
	"createdAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	CONSTRAINT "trackingEvents_pkey" PRIMARY KEY (id), 
	CONSTRAINT "trackingEvents_createdBy_users_id_fk" FOREIGN KEY("createdBy") REFERENCES users (id), 
	CONSTRAINT "trackingEvents_shipmentId_shipments_id_fk" FOREIGN KEY("shipmentId") REFERENCES shipments (id)
)



CREATE TABLE vehicles (
	id TEXT NOT NULL, 
	"carrierId" TEXT NOT NULL, 
	type "VehicleType" NOT NULL, 
	make TEXT NOT NULL, 
	model TEXT NOT NULL, 
	year INTEGER NOT NULL, 
	"licensePlate" TEXT NOT NULL, 
	color TEXT NOT NULL, 
	"maxWeightKg" DOUBLE PRECISION NOT NULL, 
	"maxVolumeM3" DOUBLE PRECISION NOT NULL, 
	"fuelType" "FuelType" DEFAULT 'GASOLINE'::"FuelType" NOT NULL, 
	mileage INTEGER DEFAULT 0 NOT NULL, 
	"isActive" BOOLEAN DEFAULT true NOT NULL, 
	"hasInsurance" BOOLEAN DEFAULT true NOT NULL, 
	"insuranceExpiry" DATE, 
	"lastMaintenance" DATE, 
	"nextMaintenance" DATE, 
	"createdAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"updatedAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	CONSTRAINT vehicles_pkey PRIMARY KEY (id), 
	CONSTRAINT "vehicles_carrierId_users_id_fk" FOREIGN KEY("carrierId") REFERENCES users (id), 
	CONSTRAINT "vehicles_licensePlate_unique" UNIQUE NULLS DISTINCT ("licensePlate")
)



CREATE TABLE invoices (
	id TEXT NOT NULL, 
	"invoiceNumber" TEXT NOT NULL, 
	"shipmentId" TEXT NOT NULL, 
	"paymentId" TEXT, 
	"issuerId" TEXT NOT NULL, 
	"recipientId" TEXT NOT NULL, 
	subtotal DOUBLE PRECISION NOT NULL, 
	"taxAmount" DOUBLE PRECISION NOT NULL, 
	"totalAmount" DOUBLE PRECISION NOT NULL, 
	currency TEXT DEFAULT 'CRC'::text NOT NULL, 
	items TEXT NOT NULL, 
	status "InvoiceStatus" DEFAULT 'DRAFT'::"InvoiceStatus" NOT NULL, 
	"issueDate" DATE NOT NULL, 
	"dueDate" DATE NOT NULL, 
	"paidDate" DATE, 
	"haciendaKey" TEXT, 
	"haciendaXml" TEXT, 
	"haciendaStatus" "HaciendaStatus" DEFAULT 'PENDING'::"HaciendaStatus", 
	"haciendaResponse" TEXT, 
	"pdfPath" TEXT, 
	"xmlPath" TEXT, 
	"createdAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"updatedAt" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	"createdBy" TEXT, 
	CONSTRAINT invoices_pkey PRIMARY KEY (id), 
	CONSTRAINT "invoices_createdBy_users_id_fk" FOREIGN KEY("createdBy") REFERENCES users (id), 
	CONSTRAINT "invoices_issuerId_users_id_fk" FOREIGN KEY("issuerId") REFERENCES users (id), 
	CONSTRAINT "invoices_paymentId_payments_id_fk" FOREIGN KEY("paymentId") REFERENCES payments (id), 
	CONSTRAINT "invoices_recipientId_users_id_fk" FOREIGN KEY("recipientId") REFERENCES users (id), 
	CONSTRAINT "invoices_shipmentId_shipments_id_fk" FOREIGN KEY("shipmentId") REFERENCES shipments (id), 
	CONSTRAINT "invoices_invoiceNumber_unique" UNIQUE NULLS DISTINCT ("invoiceNumber")
)

