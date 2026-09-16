-- schema.sql
-- Defines the structure of our products table.
-- NOTE: pgvector's CREATE EXTENSION must run once per database,
-- before any table uses the "vector" type.
--
-- Two separate embedding columns exist because they come from two
-- DIFFERENT models with different vector sizes and different meanings:
--   embedding       - text embedding (384-dim, all-MiniLM-L6-v2, Milestone 11)
--   image_embedding - CLIP embedding (512-dim, clip-ViT-B-32, Milestone 12)

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE products (
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name             TEXT NOT NULL,
    price            NUMERIC(10, 2) NOT NULL,
    currency         TEXT NOT NULL DEFAULT 'INR',
    category         TEXT NOT NULL,
    subcategory      TEXT,
    colour           TEXT NOT NULL,
    description      TEXT,
    brand            TEXT NOT NULL,
    brand_website    TEXT,
    product_url      TEXT NOT NULL,
    image_url        TEXT,
    availability     TEXT NOT NULL DEFAULT 'in_stock',
    style_tags       TEXT[],
    embedding        VECTOR(384),
    image_embedding  VECTOR(512),
    created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);