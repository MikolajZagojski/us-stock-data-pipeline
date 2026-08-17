CREATE TABLE stock_info (
    ticker VARCHAR(10) NOT NULL,
    open_price NUMERIC(19, 4) NOT NULL,
    high_price NUMERIC(19, 4) NOT NULL,
    low_price NUMERIC(19, 4) NOT NULL,
    close_price NUMERIC(19, 4) NOT NULL,
    volume NUMERIC(24, 8) NOT NULL,
    trade_day DATE NOT NULL,

    PRIMARY KEY (ticker, trade_day)
);