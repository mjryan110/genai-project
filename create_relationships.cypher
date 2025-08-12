// Create relationships between Properties and other nodes
// Run this after you have the basic nodes created

// Connect Properties to Vacancy
MATCH (p:Property), (v:Vacancy)
WHERE p.name = "Downtown Office Tower" AND v.vacancy_rate = 5.2
CREATE (p)-[:HAS_VACANCY]->(v);

MATCH (p:Property), (v:Vacancy)
WHERE p.name = "Midtown Retail Plaza" AND v.vacancy_rate = 12.8
CREATE (p)-[:HAS_VACANCY]->(v);

MATCH (p:Property), (v:Vacancy)
WHERE p.name = "Brooklyn Industrial Complex" AND v.vacancy_rate = 3.1
CREATE (p)-[:HAS_VACANCY]->(v);

MATCH (p:Property), (v:Vacancy)
WHERE p.name = "Financial District Office" AND v.vacancy_rate = 8.5
CREATE (p)-[:HAS_VACANCY]->(v);

MATCH (p:Property), (v:Vacancy)
WHERE p.name = "Queens Shopping Center" AND v.vacancy_rate = 15.2
CREATE (p)-[:HAS_VACANCY]->(v);

// Connect Properties to Financial
MATCH (p:Property), (f:Financial)
WHERE p.name = "Downtown Office Tower" AND f.cap_rate = 6.8
CREATE (p)-[:HAS_FINANCIAL]->(f);

MATCH (p:Property), (f:Financial)
WHERE p.name = "Midtown Retail Plaza" AND f.cap_rate = 5.2
CREATE (p)-[:HAS_FINANCIAL]->(f);

MATCH (p:Property), (f:Financial)
WHERE p.name = "Brooklyn Industrial Complex" AND f.cap_rate = 7.1
CREATE (p)-[:HAS_FINANCIAL]->(f);

MATCH (p:Property), (f:Financial)
WHERE p.name = "Financial District Office" AND f.cap_rate = 6.2
CREATE (p)-[:HAS_FINANCIAL]->(f);

MATCH (p:Property), (f:Financial)
WHERE p.name = "Queens Shopping Center" AND f.cap_rate = 4.8
CREATE (p)-[:HAS_FINANCIAL]->(f);

// Connect Properties to Management
MATCH (p:Property), (m:Management)
WHERE p.name = "Downtown Office Tower" AND m.manager = "CBRE"
CREATE (p)-[:MANAGED_BY]->(m);

MATCH (p:Property), (m:Management)
WHERE p.name = "Midtown Retail Plaza" AND m.manager = "CBRE"
CREATE (p)-[:MANAGED_BY]->(m);

MATCH (p:Property), (m:Management)
WHERE p.name = "Brooklyn Industrial Complex" AND m.manager = "JLL"
CREATE (p)-[:MANAGED_BY]->(m);

MATCH (p:Property), (m:Management)
WHERE p.name = "Financial District Office" AND m.manager = "CBRE"
CREATE (p)-[:MANAGED_BY]->(m);

MATCH (p:Property), (m:Management)
WHERE p.name = "Queens Shopping Center" AND m.manager = "Cushman & Wakefield"
CREATE (p)-[:MANAGED_BY]->(m);

// Connect Properties to Rental
MATCH (p:Property), (r:Rental)
WHERE p.name = "Downtown Office Tower" AND r.rental_rate = 85.50
CREATE (p)-[:HAS_RENTAL]->(r);

MATCH (p:Property), (r:Rental)
WHERE p.name = "Midtown Retail Plaza" AND r.rental_rate = 45.20
CREATE (p)-[:HAS_RENTAL]->(r);

MATCH (p:Property), (r:Rental)
WHERE p.name = "Brooklyn Industrial Complex" AND r.rental_rate = 12.80
CREATE (p)-[:HAS_RENTAL]->(r);

MATCH (p:Property), (r:Rental)
WHERE p.name = "Financial District Office" AND r.rental_rate = 92.10
CREATE (p)-[:HAS_RENTAL]->(r);

MATCH (p:Property), (r:Rental)
WHERE p.name = "Queens Shopping Center" AND r.rental_rate = 38.40
CREATE (p)-[:HAS_RENTAL]->(r);

// Connect Properties to Listing
MATCH (p:Property), (l:Listing)
WHERE p.name = "Downtown Office Tower" AND l.days_on_market = 45
CREATE (p)-[:HAS_LISTING]->(l);

MATCH (p:Property), (l:Listing)
WHERE p.name = "Midtown Retail Plaza" AND l.days_on_market = 120
CREATE (p)-[:HAS_LISTING]->(l);

MATCH (p:Property), (l:Listing)
WHERE p.name = "Brooklyn Industrial Complex" AND l.days_on_market = 30
CREATE (p)-[:HAS_LISTING]->(l);

MATCH (p:Property), (l:Listing)
WHERE p.name = "Financial District Office" AND l.days_on_market = 95
CREATE (p)-[:HAS_LISTING]->(l);

MATCH (p:Property), (l:Listing)
WHERE p.name = "Queens Shopping Center" AND l.days_on_market = 180
CREATE (p)-[:HAS_LISTING]->(l);

// Connect Properties to Lease
MATCH (p:Property), (lease:Lease)
WHERE p.name = "Downtown Office Tower" AND lease.tenant_name = "Tech Corp"
CREATE (p)-[:HAS_LEASE]->(lease);

MATCH (p:Property), (lease:Lease)
WHERE p.name = "Midtown Retail Plaza" AND lease.tenant_name = "Retail Chain"
CREATE (p)-[:HAS_LEASE]->(lease);

MATCH (p:Property), (lease:Lease)
WHERE p.name = "Brooklyn Industrial Complex" AND lease.tenant_name = "Manufacturing Inc"
CREATE (p)-[:HAS_LEASE]->(lease);

MATCH (p:Property), (lease:Lease)
WHERE p.name = "Financial District Office" AND lease.tenant_name = "Financial Services"
CREATE (p)-[:HAS_LEASE]->(lease);

MATCH (p:Property), (lease:Lease)
WHERE p.name = "Queens Shopping Center" AND lease.tenant_name = "Shopping Center Tenant"
CREATE (p)-[:HAS_LEASE]->(lease);

// Connect Properties to Valuation
MATCH (p:Property), (val:Valuation)
WHERE p.name = "Downtown Office Tower" AND val.current_value = 150000000
CREATE (p)-[:HAS_VALUATION]->(val);

MATCH (p:Property), (val:Valuation)
WHERE p.name = "Midtown Retail Plaza" AND val.current_value = 52000000
CREATE (p)-[:HAS_VALUATION]->(val);

MATCH (p:Property), (val:Valuation)
WHERE p.name = "Brooklyn Industrial Complex" AND val.current_value = 35000000
CREATE (p)-[:HAS_VALUATION]->(val);

MATCH (p:Property), (val:Valuation)
WHERE p.name = "Financial District Office" AND val.current_value = 95000000
CREATE (p)-[:HAS_VALUATION]->(val);

MATCH (p:Property), (val:Valuation)
WHERE p.name = "Queens Shopping Center" AND val.current_value = 42000000
CREATE (p)-[:HAS_VALUATION]->(val);

// Connect Properties to Amenity
MATCH (p:Property), (a:Amenity)
WHERE p.name = "Downtown Office Tower" AND a.amenity_type = "Parking"
CREATE (p)-[:HAS_AMENITY]->(a);

MATCH (p:Property), (a:Amenity)
WHERE p.name = "Midtown Retail Plaza" AND a.amenity_type = "Fitness Center"
CREATE (p)-[:HAS_AMENITY]->(a);

MATCH (p:Property), (a:Amenity)
WHERE p.name = "Brooklyn Industrial Complex" AND a.amenity_type = "Parking"
CREATE (p)-[:HAS_AMENITY]->(a);

MATCH (p:Property), (a:Amenity)
WHERE p.name = "Financial District Office" AND a.amenity_type = "Conference Rooms"
CREATE (p)-[:HAS_AMENITY]->(a);

MATCH (p:Property), (a:Amenity)
WHERE p.name = "Queens Shopping Center" AND a.amenity_type = "Restaurant"
CREATE (p)-[:HAS_AMENITY]->(a);

// Connect Properties to Certification
MATCH (p:Property), (c:Certification)
WHERE p.name = "Downtown Office Tower" AND c.certification_type = "Energy Efficiency"
CREATE (p)-[:HAS_CERTIFICATION]->(c);

MATCH (p:Property), (c:Certification)
WHERE p.name = "Midtown Retail Plaza" AND c.certification_type = "LEED"
CREATE (p)-[:HAS_CERTIFICATION]->(c);

MATCH (p:Property), (c:Certification)
WHERE p.name = "Brooklyn Industrial Complex" AND c.certification_type = "Energy Efficiency"
CREATE (p)-[:HAS_CERTIFICATION]->(c);

MATCH (p:Property), (c:Certification)
WHERE p.name = "Financial District Office" AND c.certification_type = "BREEAM"
CREATE (p)-[:HAS_CERTIFICATION]->(c);

MATCH (p:Property), (c:Certification)
WHERE p.name = "Queens Shopping Center" AND c.certification_type = "Energy Efficiency"
CREATE (p)-[:HAS_CERTIFICATION]->(c);

// Connect Properties to Maintenance
MATCH (p:Property), (main:Maintenance)
WHERE p.name = "Downtown Office Tower" AND main.maintenance_type = "HVAC"
CREATE (p)-[:HAS_MAINTENANCE]->(main);

MATCH (p:Property), (main:Maintenance)
WHERE p.name = "Midtown Retail Plaza" AND main.maintenance_type = "Plumbing"
CREATE (p)-[:HAS_MAINTENANCE]->(main);

MATCH (p:Property), (main:Maintenance)
WHERE p.name = "Brooklyn Industrial Complex" AND main.maintenance_type = "Electrical"
CREATE (p)-[:HAS_MAINTENANCE]->(main);

MATCH (p:Property), (main:Maintenance)
WHERE p.name = "Financial District Office" AND main.maintenance_type = "Roofing"
CREATE (p)-[:HAS_MAINTENANCE]->(main);

MATCH (p:Property), (main:Maintenance)
WHERE p.name = "Queens Shopping Center" AND main.maintenance_type = "HVAC"
CREATE (p)-[:HAS_MAINTENANCE]->(main);

// Connect Properties to Transportation
MATCH (p:Property), (t:Transportation)
WHERE p.name = "Downtown Office Tower" AND t.transport_type = "Subway"
CREATE (p)-[:NEAR_TRANSPORT]->(t);

MATCH (p:Property), (t:Transportation)
WHERE p.name = "Midtown Retail Plaza" AND t.transport_type = "Bus"
CREATE (p)-[:NEAR_TRANSPORT]->(t);

MATCH (p:Property), (t:Transportation)
WHERE p.name = "Brooklyn Industrial Complex" AND t.transport_type = "Train"
CREATE (p)-[:NEAR_TRANSPORT]->(t);

MATCH (p:Property), (t:Transportation)
WHERE p.name = "Financial District Office" AND t.transport_type = "Subway"
CREATE (p)-[:NEAR_TRANSPORT]->(t);

MATCH (p:Property), (t:Transportation)
WHERE p.name = "Queens Shopping Center" AND t.transport_type = "Bus"
CREATE (p)-[:NEAR_TRANSPORT]->(t);

// Connect Properties to Tax
MATCH (p:Property), (tax:Tax)
WHERE p.name = "Downtown Office Tower" AND tax.annual_tax = 2500000
CREATE (p)-[:HAS_TAX]->(tax);

MATCH (p:Property), (tax:Tax)
WHERE p.name = "Midtown Retail Plaza" AND tax.annual_tax = 850000
CREATE (p)-[:HAS_TAX]->(tax);

MATCH (p:Property), (tax:Tax)
WHERE p.name = "Brooklyn Industrial Complex" AND tax.annual_tax = 420000
CREATE (p)-[:HAS_TAX]->(tax);

MATCH (p:Property), (tax:Tax)
WHERE p.name = "Financial District Office" AND tax.annual_tax = 1800000
CREATE (p)-[:HAS_TAX]->(tax);

MATCH (p:Property), (tax:Tax)
WHERE p.name = "Queens Shopping Center" AND tax.annual_tax = 650000
CREATE (p)-[:HAS_TAX]->(tax);

// Connect Properties to Tenant
MATCH (p:Property), (tenant:Tenant)
WHERE p.name = "Downtown Office Tower" AND tenant.name = "Tech Corp"
CREATE (p)-[:HAS_TENANT]->(tenant);

MATCH (p:Property), (tenant:Tenant)
WHERE p.name = "Midtown Retail Plaza" AND tenant.name = "Retail Chain"
CREATE (p)-[:HAS_TENANT]->(tenant);

MATCH (p:Property), (tenant:Tenant)
WHERE p.name = "Brooklyn Industrial Complex" AND tenant.name = "Manufacturing Inc"
CREATE (p)-[:HAS_TENANT]->(tenant);

MATCH (p:Property), (tenant:Tenant)
WHERE p.name = "Financial District Office" AND tenant.name = "Financial Services"
CREATE (p)-[:HAS_TENANT]->(tenant);

MATCH (p:Property), (tenant:Tenant)
WHERE p.name = "Queens Shopping Center" AND tenant.name = "Shopping Center Tenant"
CREATE (p)-[:HAS_TENANT]->(tenant);

// Verify relationships were created
MATCH ()-[r]->() RETURN count(r) as total_relationships; 