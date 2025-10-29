"""
Panduan Lengkap Perintah Dasar Hadoop
Command Reference untuk operasi HDFS dan Hadoop
"""

class HadoopCommandGuide:
    def __init__(self):
        self.commands = {}
        self.setup_commands()
    
    def setup_commands(self):
        """Menyiapkan daftar command Hadoop"""
        
        # File Operations
        self.commands['file_operations'] = {
            'title': 'OPERASI FILE HDFS',
            'commands': [
                ('List direktori', 'hdfs dfs -ls /path'),
                ('List rekursif', 'hdfs dfs -ls -R /path'),
                ('Membuat direktori', 'hdfs dfs -mkdir /path'),
                ('Membuat direktori parent', 'hdfs dfs -mkdir -p /path/to/dir'),
                ('Upload file', 'hdfs dfs -put localfile.txt /hdfs/path/'),
                ('Upload direktori', 'hdfs dfs -put -r localdir/ /hdfs/path/'),
                ('Download file', 'hdfs dfs -get /hdfs/path/file.txt ./'),
                ('Download ke stdout', 'hdfs dfs -cat /hdfs/path/file.txt'),
                ('Copy dalam HDFS', 'hdfs dfs -cp /source /destination'),
                ('Move dalam HDFS', 'hdfs dfs -mv /source /destination'),
                ('Hapus file', 'hdfs dfs -rm /hdfs/path/file.txt'),
                ('Hapus direktori', 'hdfs dfs -rm -r /hdfs/path/dir'),
            ]
        }
        
        # Data Transfer
        self.commands['data_transfer'] = {
            'title': 'TRANSFER DATA',
            'commands': [
                ('Copy dari local', 'hdfs dfs -copyFromLocal local.txt /hdfs/'),
                ('Copy ke local', 'hdfs dfs -copyToLocal /hdfs/file.txt ./'),
                ('Move dari local', 'hdfs dfs -moveFromLocal local.txt /hdfs/'),
                ('Append file', 'hdfs dfs -appendToFile local.txt /hdfs/file.txt'),
                ('Merge files', 'hdfs dfs -getmerge /hdfs/dir/ output.txt'),
            ]
        }
        
        # Information
        self.commands['information'] = {
            'title': 'INFORMASI & MONITORING',
            'commands': [
                ('Disk usage', 'hdfs dfs -du -h /path'),
                ('Disk usage summary', 'hdfs dfs -du -s -h /path'),
                ('Cek space', 'hdfs dfs -df -h'),
                ('Stat file', 'hdfs dfs -stat %n,%b,%r /path/file'),
                ('Count files', 'hdfs dfs -count /path'),
                ('Checksum', 'hdfs dfs -checksum /path/file'),
                ('Find file', 'hdfs dfs -find /path -name "*.txt"'),
                ('Tail file', 'hdfs dfs -tail /path/file.txt'),
                ('Head file', 'hdfs dfs -head /path/file.txt'),
            ]
        }
        
        # Permissions
        self.commands['permissions'] = {
            'title': 'PERMISSIONS & OWNERSHIP',
            'commands': [
                ('Change mode', 'hdfs dfs -chmod 755 /path/file'),
                ('Change owner', 'hdfs dfs -chown user:group /path/file'),
                ('Change group', 'hdfs dfs -chgrp group /path/file'),
            ]
        }
        
        # Admin Commands
        self.commands['admin'] = {
            'title': 'ADMIN COMMANDS',
            'commands': [
                ('Format NameNode', 'hdfs namenode -format'),
                ('Start DFS', 'start-dfs.sh'),
                ('Stop DFS', 'stop-dfs.sh'),
                ('Start YARN', 'start-yarn.sh'),
                ('Stop YARN', 'stop-yarn.sh'),
                ('Start All', 'start-all.sh'),
                ('Stop All', 'stop-all.sh'),
                ('HDFS Report', 'hdfs dfsadmin -report'),
                ('Safe Mode Enter', 'hdfs dfsadmin -safemode enter'),
                ('Safe Mode Leave', 'hdfs dfsadmin -safemode leave'),
                ('Check Health', 'hdfs fsck /'),
            ]
        }
        
        # MapReduce
        self.commands['mapreduce'] = {
            'title': 'MAPREDUCE COMMANDS',
            'commands': [
                ('Run JAR', 'hadoop jar program.jar MainClass input output'),
                ('WordCount Example', 'hadoop jar hadoop-examples.jar wordcount /input /output'),
                ('List Jobs', 'mapred job -list'),
                ('Kill Job', 'mapred job -kill job_id'),
                ('Job Status', 'mapred job -status job_id'),
            ]
        }
    
    def print_commands(self, category=None):
        """Menampilkan command berdasarkan kategori"""
        if category and category in self.commands:
            self._print_category(category)
        else:
            # Print semua kategori
            for cat_key in self.commands:
                self._print_category(cat_key)
                print()
    
    def _print_category(self, category):
        """Print satu kategori"""
        cat_data = self.commands[category]
        print("=" * 70)
        print(f" {cat_data['title']}")
        print("=" * 70)
        
        for desc, cmd in cat_data['commands']:
            print(f"\n{desc}:")
            print(f"  $ {cmd}")
    
    def search_command(self, keyword):
        """Cari command berdasarkan keyword"""
        print(f"\n=== Hasil Pencarian: '{keyword}' ===\n")
        found = False
        
        for cat_key, cat_data in self.commands.items():
            for desc, cmd in cat_data['commands']:
                if keyword.lower() in desc.lower() or keyword.lower() in cmd.lower():
                    print(f"{desc}:")
                    print(f"  $ {cmd}\n")
                    found = True
        
        if not found:
            print(f"Tidak ditemukan command untuk '{keyword}'")

def main():
    """Main function"""
    guide = HadoopCommandGuide()
    
    print("\n" + "=" * 70)
    print(" PANDUAN PERINTAH DASAR HADOOP")
    print("=" * 70)
    print()
    
    # Print semua commands
    guide.print_commands()
    
    print("\n" + "=" * 70)
    print(" CONTOH PENGGUNAAN")
    print("=" * 70)
    print("""
# 1. Menjalankan Hadoop
$ start-all.sh

# 2. Membuat direktori dan upload file
$ hdfs dfs -mkdir -p /user/hadoop/input
$ hdfs dfs -put data.txt /user/hadoop/input/

# 3. Menjalankan WordCount
$ hadoop jar hadoop-examples.jar wordcount /user/hadoop/input /user/hadoop/output

# 4. Melihat hasil
$ hdfs dfs -cat /user/hadoop/output/part-r-00000

# 5. Download hasil
$ hdfs dfs -get /user/hadoop/output ./hasil/

# 6. Cek status
$ hdfs dfsadmin -report
    """)

if __name__ == "__main__":
    main()
