// CBRE Real Estate Dummy Data Setup
// Run this script in Neo4j to create test data for the CBRE application

// Clear existing data (optional - be careful in production!)
MATCH (n) DETACH DELETE n;

// Create Property nodes with different types
CREATE (p1:Property {
    name: "Downtown Office Tower",
    address: "123 Main Street, New York, NY",
    property_type: "Office",
    building_class: "A",
    square_feet: 500000,
    city: "New York",
    location: "downtown",
    year_built: 2010
})

CREATE (p2:Property {
    name: "Midtown Retail Plaza",
    address: "456 Broadway, New York, NY",
    property_type: "Retail",
    building_class: "B",
    square_feet: 75000,
    city: "New York",
    location: "midtown",
    year_built: 2005
})

CREATE (p3:Property {
    name: "Brooklyn Industrial Complex",
    address: "789 Industrial Ave, Brooklyn, NY",
    property_type: "Industrial",
    building_class: "C",
    square_feet: 150000,
    city: "Brooklyn",
    location: "industrial district",
    year_built: 1995
})

CREATE (p4:Property {
    name: "Financial District Office",
    address: "321 Wall Street, New York, NY",
    property_type: "Office",
    building_class: "A",
    square_feet: 300000,
    city: "New York",
    location: "financial district",
    year_built: 2015
})

CREATE (p5:Property {
    name: "Queens Shopping Center",
    address: "654 Queens Blvd, Queens, NY",
    property_type: "Retail",
    building_class: "B",
    square_feet: 120000,
    city: "Queens",
    location: "shopping center",
    year_built: 2008
});

// Create Vacancy nodes
CREATE (v1:Vacancy {vacancy_rate: 5.2, last_updated: date()})
CREATE (v2:Vacancy {vacancy_rate: 12.8, last_updated: date()})
CREATE (v3:Vacancy {vacancy_rate: 3.1, last_updated: date()})
CREATE (v4:Vacancy {vacancy_rate: 8.5, last_updated: date()})
CREATE (v5:Vacancy {vacancy_rate: 15.2, last_updated: date()});

// Create Financial nodes
CREATE (f1:Financial {cap_rate: 6.8, annual_revenue: 8500000})
CREATE (f2:Financial {cap_rate: 5.2, annual_revenue: 3200000})
CREATE (f3:Financial {cap_rate: 7.1, annual_revenue: 4200000})
CREATE (f4:Financial {cap_rate: 6.2, annual_revenue: 6800000})
CREATE (f5:Financial {cap_rate: 4.8, annual_revenue: 2800000});

// Create Management nodes
CREATE (m1:Management {manager: "CBRE", management_fee: 0.025})
CREATE (m2:Management {manager: "CBRE", management_fee: 0.030})
CREATE (m3:Management {manager: "JLL", management_fee: 0.028})
CREATE (m4:Management {manager: "CBRE", management_fee: 0.025})
CREATE (m5:Management {manager: "Cushman & Wakefield", management_fee: 0.032});

// Create Rental nodes
CREATE (r1:Rental {rental_rate: 85.50, rate_type: "per_sqft", lease_term: 60})
CREATE (r2:Rental {rental_rate: 45.20, rate_type: "per_sqft", lease_term: 36})
CREATE (r3:Rental {rental_rate: 12.80, rate_type: "per_sqft", lease_term: 48})
CREATE (r4:Rental {rental_rate: 92.10, rate_type: "per_sqft", lease_term: 72})
CREATE (r5:Rental {rental_rate: 38.40, rate_type: "per_sqft", lease_term: 24});

// Create Listing nodes
CREATE (l1:Listing {days_on_market: 45, listing_price: 125000000})
CREATE (l2:Listing {days_on_market: 120, listing_price: 45000000})
CREATE (l3:Listing {days_on_market: 30, listing_price: 28000000})
CREATE (l4:Listing {days_on_market: 95, listing_price: 89000000})
CREATE (l5:Listing {days_on_market: 180, listing_price: 32000000});

// Create Lease nodes
CREATE (lease1:Lease {tenant_name: "Tech Corp", renewal_date: date() + duration('P15D'), expiration_date: date() + duration('P2Y')})
CREATE (lease2:Lease {tenant_name: "Retail Chain", renewal_date: date() + duration('P45D'), expiration_date: date() + duration('P1Y')})
CREATE (lease3:Lease {tenant_name: "Manufacturing Inc", renewal_date: date() + duration('P90D'), expiration_date: date() + duration('P3Y')})
CREATE (lease4:Lease {tenant_name: "Financial Services", renewal_date: date() + duration('P30D'), expiration_date: date() + duration('P2Y')})
CREATE (lease5:Lease {tenant_name: "Shopping Center Tenant", renewal_date: date() + duration('P60D'), expiration_date: date() + duration('P1Y')});

// Create Valuation nodes
CREATE (val1:Valuation {current_value: 150000000, last_appraisal_date: date() - duration('P6M')})
CREATE (val2:Valuation {current_value: 52000000, last_appraisal_date: date() - duration('P1Y')})
CREATE (val3:Valuation {current_value: 35000000, last_appraisal_date: date() - duration('P8M')})
CREATE (val4:Valuation {current_value: 95000000, last_appraisal_date: date() - duration('P3M')})
CREATE (val5:Valuation {current_value: 42000000, last_appraisal_date: date() - duration('P1Y')});

// Create Amenity nodes
CREATE (a1:Amenity {amenity_type: "Parking", capacity: 500})
CREATE (a2:Amenity {amenity_type: "Fitness Center", capacity: 200})
CREATE (a3:Amenity {amenity_type: "Parking", capacity: 150})
CREATE (a4:Amenity {amenity_type: "Conference Rooms", capacity: 10})
CREATE (a5:Amenity {amenity_type: "Restaurant", capacity: 100});

// Create Certification nodes
CREATE (c1:Certification {certification_type: "Energy Efficiency", rating: 85})
CREATE (c2:Certification {certification_type: "LEED", rating: 92})
CREATE (c3:Certification {certification_type: "Energy Efficiency", rating: 78})
CREATE (c4:Certification {certification_type: "BREEAM", rating: 88})
CREATE (c5:Certification {certification_type: "Energy Efficiency", rating: 82});

// Create Maintenance nodes
CREATE (main1:Maintenance {maintenance_type: "HVAC", maintenance_date: date() - duration('P3D')})
CREATE (main2:Maintenance {maintenance_type: "Plumbing", maintenance_date: date() - duration('P1W')})
CREATE (main3:Maintenance {maintenance_type: "Electrical", maintenance_date: date() - duration('P5D')})
CREATE (main4:Maintenance {maintenance_type: "Roofing", maintenance_date: date() - duration('P2W')})
CREATE (main5:Maintenance {maintenance_type: "HVAC", maintenance_date: date() - duration('P1D')});

// Create Transportation nodes
CREATE (t1:Transportation {transport_type: "Subway", distance_meters: 150})
CREATE (t2:Transportation {transport_type: "Bus", distance_meters: 300})
CREATE (t3:Transportation {transport_type: "Train", distance_meters: 800})
CREATE (t4:Transportation {transport_type: "Subway", distance_meters: 200})
CREATE (t5:Transportation {transport_type: "Bus", distance_meters: 450});

// Create Tax nodes
CREATE (tax1:Tax {annual_tax: 2500000, tax_year: 2024})
CREATE (tax2:Tax {annual_tax: 850000, tax_year: 2024})
CREATE (tax3:Tax {annual_tax: 420000, tax_year: 2024})
CREATE (tax4:Tax {annual_tax: 1800000, tax_year: 2024})
CREATE (tax5:Tax {annual_tax: 650000, tax_year: 2024});

// Create Tenant nodes
CREATE (tenant1:Tenant {name: "Tech Corp", industry: "Technology", lease_start: date() - duration('P2Y')})
CREATE (tenant2:Tenant {name: "Retail Chain", industry: "Retail", lease_start: date() - duration('P1Y')})
CREATE (tenant3:Tenant {name: "Manufacturing Inc", industry: "Manufacturing", lease_start: date() - duration('P3Y')})
CREATE (tenant4:Tenant {name: "Financial Services", industry: "Finance", lease_start: date() - duration('P1Y')})
CREATE (tenant5:Tenant {name: "Shopping Center Tenant", industry: "Retail", lease_start: date() - duration('P6M')});

// Create relationships between Properties and other nodes
MATCH (p1:Property {name: "Downtown Office Tower"})
MATCH (p2:Property {name: "Midtown Retail Plaza"})
MATCH (p3:Property {name: "Brooklyn Industrial Complex"})
MATCH (p4:Property {name: "Financial District Office"})
MATCH (p5:Property {name: "Queens Shopping Center"})

MATCH (v1:Vacancy {vacancy_rate: 5.2})
MATCH (v2:Vacancy {vacancy_rate: 12.8})
MATCH (v3:Vacancy {vacancy_rate: 3.1})
MATCH (v4:Vacancy {vacancy_rate: 8.5})
MATCH (v5:Vacancy {vacancy_rate: 15.2})

MATCH (f1:Financial {cap_rate: 6.8})
MATCH (f2:Financial {cap_rate: 5.2})
MATCH (f3:Financial {cap_rate: 7.1})
MATCH (f4:Financial {cap_rate: 6.2})
MATCH (f5:Financial {cap_rate: 4.8})

MATCH (m1:Management {manager: "CBRE"})
MATCH (m2:Management {manager: "CBRE"})
MATCH (m3:Management {manager: "JLL"})
MATCH (m4:Management {manager: "CBRE"})
MATCH (m5:Management {manager: "Cushman & Wakefield"})

MATCH (r1:Rental {rental_rate: 85.50})
MATCH (r2:Rental {rental_rate: 45.20})
MATCH (r3:Rental {rental_rate: 12.80})
MATCH (r4:Rental {rental_rate: 92.10})
MATCH (r5:Rental {rental_rate: 38.40})

MATCH (l1:Listing {days_on_market: 45})
MATCH (l2:Listing {days_on_market: 120})
MATCH (l3:Listing {days_on_market: 30})
MATCH (l4:Listing {days_on_market: 95})
MATCH (l5:Listing {days_on_market: 180})

MATCH (lease1:Lease {tenant_name: "Tech Corp"})
MATCH (lease2:Lease {tenant_name: "Retail Chain"})
MATCH (lease3:Lease {tenant_name: "Manufacturing Inc"})
MATCH (lease4:Lease {tenant_name: "Financial Services"})
MATCH (lease5:Lease {tenant_name: "Shopping Center Tenant"})

MATCH (val1:Valuation {current_value: 150000000})
MATCH (val2:Valuation {current_value: 52000000})
MATCH (val3:Valuation {current_value: 35000000})
MATCH (val4:Valuation {current_value: 95000000})
MATCH (val5:Valuation {current_value: 42000000})

MATCH (a1:Amenity {amenity_type: "Parking"})
MATCH (a2:Amenity {amenity_type: "Fitness Center"})
MATCH (a3:Amenity {amenity_type: "Parking"})
MATCH (a4:Amenity {amenity_type: "Conference Rooms"})
MATCH (a5:Amenity {amenity_type: "Restaurant"})

MATCH (c1:Certification {certification_type: "Energy Efficiency"})
MATCH (c2:Certification {certification_type: "LEED"})
MATCH (c3:Certification {certification_type: "Energy Efficiency"})
MATCH (c4:Certification {certification_type: "BREEAM"})
MATCH (c5:Certification {certification_type: "Energy Efficiency"})

MATCH (main1:Maintenance {maintenance_type: "HVAC"})
MATCH (main2:Maintenance {maintenance_type: "Plumbing"})
MATCH (main3:Maintenance {maintenance_type: "Electrical"})
MATCH (main4:Maintenance {maintenance_type: "Roofing"})
MATCH (main5:Maintenance {maintenance_type: "HVAC"})

MATCH (t1:Transportation {transport_type: "Subway"})
MATCH (t2:Transportation {transport_type: "Bus"})
MATCH (t3:Transportation {transport_type: "Train"})
MATCH (t4:Transportation {transport_type: "Subway"})
MATCH (t5:Transportation {transport_type: "Bus"})

MATCH (tax1:Tax {annual_tax: 2500000})
MATCH (tax2:Tax {annual_tax: 850000})
MATCH (tax3:Tax {annual_tax: 420000})
MATCH (tax4:Tax {annual_tax: 1800000})
MATCH (tax5:Tax {annual_tax: 650000})

MATCH (tenant1:Tenant {name: "Tech Corp"})
MATCH (tenant2:Tenant {name: "Retail Chain"})
MATCH (tenant3:Tenant {name: "Manufacturing Inc"})
MATCH (tenant4:Tenant {name: "Financial Services"})
MATCH (tenant5:Tenant {name: "Shopping Center Tenant"})

// Create relationships
CREATE (p1)-[:HAS_VACANCY]->(v1)
CREATE (p2)-[:HAS_VACANCY]->(v2)
CREATE (p3)-[:HAS_VACANCY]->(v3)
CREATE (p4)-[:HAS_VACANCY]->(v4)
CREATE (p5)-[:HAS_VACANCY]->(v5)

CREATE (p1)-[:HAS_FINANCIAL]->(f1)
CREATE (p2)-[:HAS_FINANCIAL]->(f2)
CREATE (p3)-[:HAS_FINANCIAL]->(f3)
CREATE (p4)-[:HAS_FINANCIAL]->(f4)
CREATE (p5)-[:HAS_FINANCIAL]->(f5)

CREATE (p1)-[:MANAGED_BY]->(m1)
CREATE (p2)-[:MANAGED_BY]->(m2)
CREATE (p3)-[:MANAGED_BY]->(m3)
CREATE (p4)-[:MANAGED_BY]->(m4)
CREATE (p5)-[:MANAGED_BY]->(m5)

CREATE (p1)-[:HAS_RENTAL]->(r1)
CREATE (p2)-[:HAS_RENTAL]->(r2)
CREATE (p3)-[:HAS_RENTAL]->(r3)
CREATE (p4)-[:HAS_RENTAL]->(r4)
CREATE (p5)-[:HAS_RENTAL]->(r5)

CREATE (p1)-[:HAS_LISTING]->(l1)
CREATE (p2)-[:HAS_LISTING]->(l2)
CREATE (p3)-[:HAS_LISTING]->(l3)
CREATE (p4)-[:HAS_LISTING]->(l4)
CREATE (p5)-[:HAS_LISTING]->(l5)

CREATE (p1)-[:HAS_LEASE]->(lease1)
CREATE (p2)-[:HAS_LEASE]->(lease2)
CREATE (p3)-[:HAS_LEASE]->(lease3)
CREATE (p4)-[:HAS_LEASE]->(lease4)
CREATE (p5)-[:HAS_LEASE]->(lease5)

CREATE (p1)-[:HAS_VALUATION]->(val1)
CREATE (p2)-[:HAS_VALUATION]->(val2)
CREATE (p3)-[:HAS_VALUATION]->(val3)
CREATE (p4)-[:HAS_VALUATION]->(val4)
CREATE (p5)-[:HAS_VALUATION]->(val5)

CREATE (p1)-[:HAS_AMENITY]->(a1)
CREATE (p2)-[:HAS_AMENITY]->(a2)
CREATE (p3)-[:HAS_AMENITY]->(a3)
CREATE (p4)-[:HAS_AMENITY]->(a4)
CREATE (p5)-[:HAS_AMENITY]->(a5)

CREATE (p1)-[:HAS_CERTIFICATION]->(c1)
CREATE (p2)-[:HAS_CERTIFICATION]->(c2)
CREATE (p3)-[:HAS_CERTIFICATION]->(c3)
CREATE (p4)-[:HAS_CERTIFICATION]->(c4)
CREATE (p5)-[:HAS_CERTIFICATION]->(c5)

CREATE (p1)-[:HAS_MAINTENANCE]->(main1)
CREATE (p2)-[:HAS_MAINTENANCE]->(main2)
CREATE (p3)-[:HAS_MAINTENANCE]->(main3)
CREATE (p4)-[:HAS_MAINTENANCE]->(main4)
CREATE (p5)-[:HAS_MAINTENANCE]->(main5)

CREATE (p1)-[:NEAR_TRANSPORT]->(t1)
CREATE (p2)-[:NEAR_TRANSPORT]->(t2)
CREATE (p3)-[:NEAR_TRANSPORT]->(t3)
CREATE (p4)-[:NEAR_TRANSPORT]->(t4)
CREATE (p5)-[:NEAR_TRANSPORT]->(t5)

CREATE (p1)-[:HAS_TAX]->(tax1)
CREATE (p2)-[:HAS_TAX]->(tax2)
CREATE (p3)-[:HAS_TAX]->(tax3)
CREATE (p4)-[:HAS_TAX]->(tax4)
CREATE (p5)-[:HAS_TAX]->(tax5)

CREATE (p1)-[:HAS_TENANT]->(tenant1)
CREATE (p2)-[:HAS_TENANT]->(tenant2)
CREATE (p3)-[:HAS_TENANT]->(tenant3)
CREATE (p4)-[:HAS_TENANT]->(tenant4)
CREATE (p5)-[:HAS_TENANT]->(tenant5);

// Create some additional relationships for more complex queries
CREATE (p1)-[:HAS_TENANT]->(tenant4)
CREATE (p4)-[:HAS_TENANT]->(tenant1)
CREATE (p2)-[:HAS_TENANT]->(tenant5);

// Add some additional amenities to properties
CREATE (p1)-[:HAS_AMENITY]->(a4)
CREATE (p4)-[:HAS_AMENITY]->(a1)
CREATE (p4)-[:HAS_AMENITY]->(a2);

// Add some additional maintenance records
CREATE (p1)-[:HAS_MAINTENANCE]->(main2)
CREATE (p3)-[:HAS_MAINTENANCE]->(main1);

// Verify the data was created
MATCH (n) RETURN count(n) as total_nodes;
MATCH ()-[r]->() RETURN count(r) as total_relationships; 