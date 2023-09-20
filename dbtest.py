import psycopg2

def test_connection():
    cursor = None
    connection = None
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="hakkoda.postgres.database.azure.com",
            port="5432",
            user="hakkoda",
            password="P@ssw0rd",
            dbname="postgres"
        )

        # Create a cursor object using the connection
        cursor = connection.cursor()
        
        # Execute a simple query to create the table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS factset_apis (
            id SERIAL PRIMARY KEY,
            category VARCHAR(255),
            name VARCHAR(255),
            description TEXT,
            type VARCHAR(50)
        )
        """)
        
        apis_data = [
    ('Analytics', 'Analytics Datastore API', 'Request pre-calculated Portfolio Analytics data saved in FactSet\'s Analytics Datastore, via deterministic URLs.', 'Connected Recipes'),
    ('Analytics', 'Axioma Equity Optimizer API', 'The Axioma Equity API offers equity-based portfolio optimizations, balancing a client’s investment objectives within the confines of the established constraints within their investment strategy.', 'Analytics'),
    ('Analytics', 'Axioma Fixed Income Optimizer', 'Fixed Income-based portfolio optimization', 'Analytics'),
    ('Analytics', 'Barra Portfolio Optimizer', 'Barra Portfolio Optimizer (BPM) API', 'Functional'),
    ('Functional', 'Bonds API for Digital Portals', 'Search for fixed income instruments, using a criteria-based screener. The API provides also fundamental data and key figures.', 'Functional'),
    ('Utility', 'BookBuilder API', 'The BookBuilder API is a powerful tool that quickly combines FactSet’s detailed reports for companies of interest into polished pdfs that can be read, saved down, and shared with others.', 'Connected Recipes'),
    ('Content', 'Capital Structure Report Builder API', 'Curated data from multiple sources for comprehensive capital analysis reports', 'Functional'),
    ('Functional', 'Chart Generation Service', 'An API for getting chart images in the form of png or jpg based on various parameters like ticker, benchmark, currency, frequency, start and end date etc.', 'Functional'),
    ('Content', 'Classifications API', 'Get Industry Classifications from a variety of vendors', 'Functional'),
    ('Functional', 'Company Logo API for Digital Portals', 'Logo images of listed companies (US, CA, EU)', 'Content'),
     ('Content', 'Content Feeds Data Dictionary', 'Browse data items and definitions available through FactSet\'s off platform product offerings.', 'Content'),
    ('Content', 'Data Monitor API', 'Data Monitor is an SDK that provides access to the same, trusted, information available within FactSet\'s Workstation and Web offerings.', 'Connected Recipes'),
    ('Content', 'Direct Streaming of Transaction Messages API', 'Connect transaction data from your OMS to be leveraged in FactSet\'s PMP and Portfolio Analytics applications', 'Analytics'),
    ('Content', 'Documents Distributor - CallStreet Events', 'CallStreet Events contains all the Documents Distributor APIs that offer events data such as Events Audio and Near Real-Time Transcripts.', 'Content'),
    ('Content', 'Documents Distributor - Documents API', 'Documents APIs that provide filings such as Global Filings and XML files such as StreetAccount', 'Content'),
    ('Content', 'ETF Profile and Prices API', 'Access FactSet-collected profile data and pricing for Exchange Traded Funds (ETFs).', 'Content'),
    ('Content', 'Event Calendar API', 'Accessing Event Calendar content along with business logic contained in the workstation experience', 'Content'),
    ('Content', 'Exchange DataFeed Data Model API', 'The Exchange DataFeed Data Model API provides mapping tables for enumeration values used in the FactSet Real-Time products', 'Content'),
    ('Content', 'Exchange DataFeed Snapshot API - Entire Exchange', 'Provides clients access to Snapshot files created at one-hour intervals for an entire exchange', 'Content'),
    ('Content', 'Exchange DataFeed Snapshot API - Symbol List', 'FactSet’s Exchange DataFeed Snapshot API provides cost-effective access to real-time and delayed global exchange data. Proprietary technology normalizes over 200 global exchanges and 150+ data fields. Asset types integrated include equities, …', 'Content'),
    ('Content', 'FactSet Benchmarks API', 'Returns Benchmark Constituent data including weights, price, and market value for a specified date.', 'Functional'),
    ('Content', 'FactSet Concordance API', 'The FactSet Concordance API helps our users discover the respective FactSet Entity & People identifier for a specific entity based off of a list of provided corresponding attributes, such as Names, URLs, and Location.', 'Content'),
    ('Content', 'FactSet Digital Cards', 'The FactSet Digital Cards API provides quick access to key company information and market data in an easily consumable and sharable format.', 'Content'),
    ('Content', 'FactSet ESG API', 'FactSet ESG API giving access to SASB & SDG Score data', 'Connected Recipes'),
    ('Content', 'FactSet ETF API', 'ETF Reference Data', 'Content'),
    ('Content', 'FactSet Entity API', 'FactSet’s Entity API provides access to FactSet’s complete security and entity level symbology, comprehensive entity reference data, and all of the necessary relationships and connections to create a foundation that tightly correlates disparate sources o', 'Connected Recipes'),
    ('Content', 'FactSet Entity Report Builder API', 'Create entity tree reports that display complex ownership structures through the FactSet Entity Report Builder API.', 'Content'),
    ('Content', 'FactSet Estimates API', '20+ years of comprehensive estimates and statistics on a wide variety of financial statement items as well as industry-specific metrics. FactSet’s consensus estimates are aggregated from a wide base of contributors and cover over 19,000 active…', 'Connected Recipes'),
    ('Content', 'FactSet Estimates Report Builder API', 'The FactSet Estimates Report Builder APIs return consensus estimate data with fiscal periods and line items structured in a presentation-ready format.', 'Content'),
    ('Content', 'FactSet Fundamentals API', 'Gain access to current, comprehensive, and comparative information on securities in worldwide developed and emerging markets. Composed of annual and interim/quarterly data and detailed historical financial statement content, FactSet Fundamentals…', 'Connected Recipes'),
    ('Content', 'FactSet Fundamentals Report Builder API', 'Report Builder APIs return data in relational structures and with industry handling to provide the most relevant financial data in a presentation-ready format.', 'Content'),
    ('Content', 'FactSet Funds API', 'Reference and Time Series Mutual Fund Data', 'Content'),
    ('Content', 'FactSet GeoRev API', 'FactSet Revere Geographic Revenue ("GeoRev") Exposure data provides a highly structured and normalized display of companies’ revenues by geography.', 'Content'),
    ('Content', 'FactSet Global Prices API', 'FactSet Global Prices API currently covers listing and composite level prices, volume, turnover, and VWAP data on a seven day week basis for a global equity universe.', 'Content'),
    ('Content', 'FactSet Intraday Tick History API', 'FactSet’s Tick History provides cost-effective access to consolidated real-time and delayed global exchange data. Proprietary technology normalizes data from over 200 global exchanges and across 19 tick history fields. Asset types integrated…', 'Content'),
    ('Content', 'FactSet Options API', 'The FactSet Options API provides Chains and related pricing data such as mid bid-ask price, reference data (e.g., strike price), and risk measures (e.g., Greeks and implied volatility).', 'Content'),
    ('Content', 'FactSet Ownership API', 'FactSet’s Fund Ownership API gives access to underlying fund holding details for a specified fund ID or list of IDs. Holdings details include industry codes, security identifiers, adjusted market value, adjusted shares held, and issue type.', 'Content'),
    ('Content', 'FactSet Ownership Report Builder API', 'Returns top holders of company and fund equity', 'Content'),
    ('Content', 'FactSet People API', 'Fetch People Profiles, Job History, or get associated positions and names of companies.', 'Analytics'),
    ('Content', 'FactSet Portfolio Optimizer API', 'The FactSet Portfolio Optimizer (FPO) offers full multi-asset class portfolio optimization, balancing a client’s investment objectives within the confines of the established constraints within the investment strategy.', 'Content'),
    ('Content', 'FactSet Prices API', 'Gain access to comprehensive global coverage for equity prices, returns, volume, shares, splits, and dividends. Security types include Common Stock, ADR, GDR, Preferred, Closed-ended Fund, Exchange Traded Fund, Unit, Open-ended Fund, Exchange…', 'Connected Recipes'),
    ('Content', 'FactSet Private Markets API', 'FactSet Private Markets API', 'Content'),
    ('Content', 'FactSet Programmatic Environment API', 'FactSet Programmatic Environment API', 'Analytics'),
    ('Content', 'FactSet Quant Factor Library API', 'The FactSet Quant Factor Library (QFL) API helps to detect investment themes across global equity markets, incorporate ideas into your portfolio construction process, and transform raw data into actionable intelligence.', 'Content'),
    ('Content', 'FactSet RBICS API', 'A Comprehensive structured taxonomy to classify companies by what they primarily do. FactSet Revere Business Industry Classification System (RBICS) delivers a granular view for investors by classifying companies using a bottom-up approach…', 'Utility'),
    ('Content', 'FactSet Search Answers', 'The FactSet Search Answers API provides answers to search queries, reflecting the data shown within FactSet Search Answers.', 'Content'),
    ('Content', 'FactSet Terms and Conditions API', 'FactSet Security Reference - Fixed Income Terms & Conditions', 'Content'),
    ('Content', 'FactSet Tick History API', 'Tick History provides dynamic access to historical tick data for a specific security for specific dates or date range.', 'Content'),
    ('Content', 'FactSet Trading API', 'This Trading API gives programmatic access to FactSet\'s trading platform', 'Functional'),
    ('Content', 'FactSet Universal Screening API', 'Use the Universal Screening API to calculate your saved screens and then output the results in a convenient JSON format or archive the results to an Open FactSet Database (OFDB) file', 'Functional'),
    # ... continue with the next APIs ...
        for data in apis_data:
            cursor.execute("""
            INSERT INTO factset_apis (category, name, description, type)
            VALUES (%s, %s, %s, %s)
            """, data)

        connection.commit()

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    test_connection()
