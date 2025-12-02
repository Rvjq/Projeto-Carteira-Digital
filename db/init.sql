USE wallet_homolog;

-- =========================================================
--  Tabelas (Aluno deve fazer o modelo)
-- =========================================================


CREATE TABLE IF NOT EXISTS carteira (
    endereco_carteira VARCHAR(32) PRIMARY KEY,
    hash_chave_privada VARCHAR(64) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TINYINT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS moeda (
    id_moeda SMALLINT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10),
    nome VARCHAR(50),
    tipo VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS saldo_carteira (
    endereco_carteira VARCHAR(32) NOT NULL,
    id_moeda SMALLINT NOT NULL,
    saldo DECIMAL(18,8) DEFAULT 0,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (endereco_carteira, id_moeda),
    FOREIGN KEY (endereco_carteira) REFERENCES carteira(endereco_carteira),
    FOREIGN KEY (id_moeda) REFERENCES moeda(id_moeda)
);

CREATE TABLE IF NOT EXISTS deposito_saque (
    id_movimento BIGINT AUTO_INCREMENT PRIMARY KEY,
    endereco_carteira VARCHAR(32) NOT NULL,
    id_moeda SMALLINT NOT NULL,
    tipo VARCHAR(20),
    valor DECIMAL(18,8) NOT NULL,
    taxa_valor DECIMAL(18,8) NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (endereco_carteira) REFERENCES carteira(endereco_carteira),
    FOREIGN KEY (id_moeda) REFERENCES moeda(id_moeda)
);

CREATE TABLE IF NOT EXISTS conversao (
    id_conversao BIGINT AUTO_INCREMENT PRIMARY KEY,
    endereco_carteira VARCHAR(32) NOT NULL,
    id_moeda_origem SMALLINT NOT NULL,
    id_moeda_destino SMALLINT NOT NULL,
    valor_origem DECIMAL(18,8) NOT NULL,
    valor_destino DECIMAL(18,8) NOT NULL,
    taxa_percentual DECIMAL(18,8) NOT NULL,
    taxa_valor DECIMAL(18,8) NOT NULL,
    cotacao_utilizada DECIMAL(18,8) NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (endereco_carteira) REFERENCES carteira(endereco_carteira),
    FOREIGN KEY (id_moeda_origem) REFERENCES moeda(id_moeda),
    FOREIGN KEY (id_moeda_destino) REFERENCES moeda(id_moeda)
);

CREATE TABLE IF NOT EXISTS transferencia (
    id_transferencia BIGINT AUTO_INCREMENT PRIMARY KEY,
    endereco_origem VARCHAR(32) NOT NULL,
    endereco_destino VARCHAR(32) NOT NULL,
    id_moeda SMALLINT NOT NULL,
    valor DECIMAL(18,8) NOT NULL,
    taxa_valor DECIMAL(18,8) NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (endereco_origem) REFERENCES carteira(endereco_carteira),
    FOREIGN KEY (endereco_destino) REFERENCES carteira(endereco_carteira),
    FOREIGN KEY (id_moeda) REFERENCES moeda(id_moeda)
);

-- =========================================================
--  Popular Tabelas
-- =========================================================

INSERT INTO moeda (codigo, nome, tipo) VALUES
('BTC', 'Bitcoin', 'CRYPTO'),
('ETH', 'Ethereum', 'CRYPTO'),
('SOL', 'Solana', 'CRYPTO'),
('USD', 'Dolar Americano', 'FIAT'),
('BRL', 'Real', 'FIAT');