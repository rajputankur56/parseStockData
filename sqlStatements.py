from getConnection import update_none


CREATE_COMPUTER_TECHNOLOGY_TABLES = [
    '''
    DROP TABLE IF EXISTS MB_Sector_Computer_Technology
    ''',
    '''
    CREATE TABLE IF NOT EXISTS MB_Sector_Computer_Technology
    (
    id int PRIMARY KEY AUTO_INCREMENT,
    Rank_row VARCHAR(10),
    Name VARCHAR(100),
    Symbol VARCHAR(20),
    Stock_Price VARCHAR(200),
    Market_Cap VARCHAR(100),
    PE_Ratio DECIMAL(20, 2),
    Dividend_Yield DECIMAL(20, 2),
    Consensus_Rating TEXT,
    Consensus_Price_Target VARCHAR(200)
    );
    '''
]

def add_mb_sector_computer_technology_data(*args):
    Rank, Name, Symbol, Stock_Price, Market_Cap, PE_Ratio, Dividend_Yield, Consensus_Rating, Consensus_Price_Target = args

    insertQuery = f'''
    INSERT INTO MB_Sector_Computer_Technology
    (Rank_row, Name, Symbol, Stock_Price, Market_Cap, PE_Ratio, Dividend_Yield, Consensus_Rating, Consensus_Price_Target)
    VALUES ('{Rank}', '{Name}', '{Symbol}', '{Stock_Price}', '{Market_Cap}', {PE_Ratio}, {Dividend_Yield}, '{Consensus_Rating}', '{Consensus_Price_Target}');
    '''

    return insertQuery

