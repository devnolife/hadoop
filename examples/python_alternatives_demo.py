"""
ALTERNATIF: Big Data Processing dengan Dask (Pure Python)
TIDAK MEMERLUKAN Java atau Hadoop!
"""

def demo_dask():
    """
    Dask adalah alternatif Python untuk big data processing
    Tidak memerlukan Java sama sekali!
    """
    
    print("=" * 70)
    print("DASK - ALTERNATIF PYTHON UNTUK BIG DATA (NO JAVA!)")
    print("=" * 70)
    print()
    
    try:
        import dask.dataframe as dd
        import dask.bag as db
        import pandas as pd
        
        print("✓ Dask terinstall!\n")
        
        # 1. Buat sample data
        print("1. Membuat sample data...")
        data = {
            'id': range(1, 1001),
            'name': [f'User{i}' for i in range(1, 1001)],
            'value': [i * 10 for i in range(1, 1001)]
        }
        df = pd.DataFrame(data)
        df.to_csv('sample_big_data.csv', index=False)
        print("   ✓ Created sample_big_data.csv")
        
        # 2. Load dengan Dask (untuk file besar)
        print("\n2. Load data dengan Dask...")
        ddf = dd.read_csv('sample_big_data.csv')
        print(f"   ✓ Loaded {len(ddf)} rows")
        print(f"   Columns: {list(ddf.columns)}")
        
        # 3. Processing
        print("\n3. Processing data...")
        result = ddf[ddf['value'] > 500].compute()
        print(f"   ✓ Filtered: {len(result)} rows with value > 500")
        
        # 4. Aggregation
        print("\n4. Aggregation...")
        total = ddf['value'].sum().compute()
        mean_val = ddf['value'].mean().compute()
        print(f"   ✓ Total: {total}")
        print(f"   ✓ Mean: {mean_val:.2f}")
        
        # 5. Word Count (seperti MapReduce)
        print("\n5. Word Count (MapReduce style)...")
        text = [
            "Hello world",
            "Big data processing",
            "Hello Python",
            "Data science",
            "Big data analytics"
        ]
        
        bag = db.from_sequence(text)
        word_count = (bag
                     .str.lower()
                     .str.split()
                     .flatten()
                     .frequencies()
                     .compute())
        
        print("   ✓ Word frequencies:")
        for word, count in sorted(word_count.items()):
            print(f"      {word}: {count}")
        
        print("\n" + "=" * 70)
        print("✅ Dask berhasil! Pure Python, NO JAVA needed!")
        print("=" * 70)
        
    except ImportError:
        print("✗ Dask belum terinstall")
        print("\nInstall dengan:")
        print("  pip install dask[complete]")
        print("\nDask Features:")
        print("  ✓ Pure Python - NO Java needed!")
        print("  ✓ Parallel computing")
        print("  ✓ Handle dataset lebih besar dari RAM")
        print("  ✓ Pandas-like API")
        print("  ✓ Distributed computing")


def demo_pandas_chunking():
    """
    Pandas dengan chunking untuk file besar
    Alternatif paling simple tanpa library tambahan
    """
    
    print("\n" + "=" * 70)
    print("PANDAS CHUNKING - PROSES FILE BESAR (NO JAVA!)")
    print("=" * 70)
    print()
    
    try:
        import pandas as pd
        
        # Buat sample data
        print("1. Membuat large file...")
        data = {
            'id': range(1, 10001),
            'value': range(10000, 20000)
        }
        pd.DataFrame(data).to_csv('large_file.csv', index=False)
        print("   ✓ Created large_file.csv (10,000 rows)")
        
        # Process in chunks
        print("\n2. Processing in chunks...")
        chunk_size = 1000
        total_sum = 0
        row_count = 0
        
        for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
            total_sum += chunk['value'].sum()
            row_count += len(chunk)
            print(f"   Processed chunk: {row_count} rows")
        
        print(f"\n   ✓ Total rows: {row_count}")
        print(f"   ✓ Sum: {total_sum}")
        
        print("\n" + "=" * 70)
        print("✅ Pandas chunking berhasil! NO JAVA needed!")
        print("=" * 70)
        
    except ImportError:
        print("✗ Pandas belum terinstall")
        print("  pip install pandas")


def show_alternatives():
    """Menampilkan semua alternatif"""
    print("\n" + "=" * 70)
    print("ALTERNATIF BIG DATA PROCESSING TANPA JAVA")
    print("=" * 70)
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║  OPSI 1: Dask (Recommended!)                                      ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✓ Pure Python - NO Java!                                         ║
║  ✓ Parallel & distributed computing                               ║
║  ✓ Pandas-like API                                                ║
║  ✓ Handle data lebih besar dari RAM                               ║
║                                                                    ║
║  Install: pip install dask[complete]                              ║
╚═══════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════╗
║  OPSI 2: Pandas Chunking                                          ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✓ Built-in Pandas - NO extra install                             ║
║  ✓ Simple untuk dataset sedang                                    ║
║  ✓ Process file by chunks                                         ║
║                                                                    ║
║  Install: pip install pandas                                      ║
╚═══════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════╗
║  OPSI 3: Mock HDFS (File system simulation)                       ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✓ Pure Python - NO dependencies                                  ║
║  ✓ Simulasi HDFS operations                                       ║
║  ✓ Bagus untuk learning & testing                                 ║
║                                                                    ║
║  No install needed - Pure Python!                                 ║
╚═══════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════╗
║  OPSI 4: Vaex                                                     ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✓ Out-of-core DataFrames                                         ║
║  ✓ Sangat cepat untuk visualisasi                                 ║
║  ✓ Memory efficient                                               ║
║                                                                    ║
║  Install: pip install vaex                                        ║
╚═══════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════╗
║  OPSI 5: Polars                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✓ Super fast DataFrame library                                   ║
║  ✓ Rust-based but Python API                                      ║
║  ✓ Lazy evaluation                                                ║
║                                                                    ║
║  Install: pip install polars                                      ║
╚═══════════════════════════════════════════════════════════════════╝

KESIMPULAN:
-----------
✗ Hadoop = PERLU Java (requirement wajib)
✓ Alternatif Python = TIDAK perlu Java!

Untuk tugas kuliah, Anda bisa:
1. Install Java + Hadoop (cara resmi)
2. ATAU gunakan alternatif Python di atas (lebih mudah!)
    """)


if __name__ == "__main__":
    show_alternatives()
    
    print("\n" + "=" * 70)
    print("DEMO PRAKTIS")
    print("=" * 70)
    
    demo_dask()
    demo_pandas_chunking()
