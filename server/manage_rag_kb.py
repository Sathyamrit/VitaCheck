#!/usr/bin/env python3
"""
RAG Knowledge Base Management
List, delete, clear, export ChromaDB data
Reset to default or switch contexts
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict

from vector_store import vector_store
from micronutrient_kb import MICRONUTRIENT_DB


class KBManager:
    """Manage ChromaDB knowledge base"""
    
    def __init__(self):
        self.vector_store = vector_store
    
    def list_items(self) -> List[Dict]:
        """List all items in vector store"""
        print("\n[INFO] Fetching items from vector store...")
        
        try:
            # Get all items from collection
            results = self.vector_store.collection.get(
                include=['metadatas', 'documents']
            )
            
            items = []
            if results['metadatas']:
                for metadata in results['metadatas']:
                    items.append(metadata)
            
            print(f"\n[OK] Found {len(items)} items in knowledge base:")
            print("="*70)
            
            for i, item in enumerate(items, 1):
                print(f"{i}. {item.get('name', 'N/A')} ({item.get('category', 'N/A')})")
            
            return items
            
        except Exception as e:
            print(f"[ERROR] Failed to list items: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        print("\n[INFO] Calculating KB statistics...")
        
        try:
            count = self.vector_store.collection.count()
            
            # Get all metadatas
            results = self.vector_store.collection.get(include=['metadatas'])
            
            categories = {}
            if results['metadatas']:
                for metadata in results['metadatas']:
                    cat = metadata.get('category', 'Unknown')
                    categories[cat] = categories.get(cat, 0) + 1
            
            stats = {
                'total_items': count,
                'categories': categories,
                'storage_path': './chroma_db',
            }
            
            print("\n[OK] KB STATISTICS:")
            print("="*70)
            print(f"Total Items: {stats['total_items']}")
            print(f"Categories:")
            for cat, count in stats['categories'].items():
                print(f"  • {cat}: {count}")
            
            return stats
            
        except Exception as e:
            print(f"[ERROR] Failed to get stats: {e}")
            return {}
    
    def delete_item(self, item_id: str) -> bool:
        """Delete specific item by ID"""
        print(f"\n[INFO] Deleting item: {item_id}")
        
        try:
            self.vector_store.collection.delete(ids=[item_id])
            print(f"[OK] Item deleted: {item_id}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete item: {e}")
            return False
    
    def delete_category(self, category: str) -> int:
        """Delete all items in a category"""
        print(f"\n[WARNING] Deleting all items in category: {category}")
        
        # Get all items in category
        try:
            results = self.vector_store.collection.get(include=['metadatas'])
            
            to_delete = []
            if results['ids'] and results['metadatas']:
                for idx, metadata in enumerate(results['metadatas']):
                    if metadata.get('category') == category:
                        to_delete.append(results['ids'][idx])
            
            if to_delete:
                self.vector_store.collection.delete(ids=to_delete)
                print(f"[OK] Deleted {len(to_delete)} items from category: {category}")
                return len(to_delete)
            else:
                print(f"[INFO] No items found in category: {category}")
                return 0
                
        except Exception as e:
            print(f"[ERROR] Failed to delete category: {e}")
            return 0
    
    def clear_all(self, confirm: bool = False) -> bool:
        """Clear all data from vector store"""
        if not confirm:
            print("\n[WARNING] This will DELETE ALL data from ChromaDB!")
            response = input("Type 'yes' to confirm: ")
            if response.lower() != 'yes':
                print("[INFO] Operation cancelled")
                return False
        
        print("\n[INFO] Clearing all items from vector store...")
        
        try:
            # Get all IDs and delete them
            results = self.vector_store.collection.get()
            if results['ids']:
                self.vector_store.collection.delete(ids=results['ids'])
                print(f"[OK] Deleted {len(results['ids'])} items")
            else:
                print("[INFO] No items to delete")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to clear: {e}")
            return False
    
    def reset_to_default(self, confirm: bool = False) -> bool:
        """Reset to default micronutrients"""
        if not confirm:
            print("\n[WARNING] This will CLEAR and RESET to default 5 micronutrients!")
            response = input("Type 'yes' to confirm: ")
            if response.lower() != 'yes':
                print("[INFO] Operation cancelled")
                return False
        
        print("\n[INFO] Resetting to default micronutrients...")
        
        # Clear all
        try:
            results = self.vector_store.collection.get()
            if results['ids']:
                self.vector_store.collection.delete(ids=results['ids'])
                print("[OK] Cleared existing data")
        except:
            pass
        
        # Re-initialize with defaults
        try:
            self.vector_store.is_initialized = False
            self.vector_store.initialize()
            print("[OK] Reset complete - default micronutrients loaded")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to reset: {e}")
            return False
    
    def export(self, filepath: str) -> bool:
        """Export KB to JSON file"""
        print(f"\n[INFO] Exporting knowledge base to: {filepath}")
        
        try:
            results = self.vector_store.collection.get(
                include=['metadatas', 'documents']
            )
            
            export_data = {
                'metadata': results.get('metadatas', []),
                'documents': results.get('documents', []),
                'count': len(results.get('ids', []))
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"[OK] Exported {export_data['count']} items to {filepath}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to export: {e}")
            return False
    
    def delete_collection(self, confirm: bool = False) -> bool:
        """Delete entire ChromaDB collection and storage"""
        if not confirm:
            print("\n[WARNING] This will DELETE the entire ChromaDB collection and storage!")
            response = input("Type 'yes' to confirm: ")
            if response.lower() != 'yes':
                print("[INFO] Operation cancelled")
                return False
        
        print("\n[INFO] Deleting ChromaDB collection...")
        
        try:
            self.vector_store.client.delete_collection(name="micronutrients")
            print("[OK] Collection deleted")
            
            # Remove storage directory
            import shutil
            if Path('./chroma_db').exists():
                shutil.rmtree('./chroma_db')
                print("[OK] Storage directory removed")
            
            # Reinitialize
            from vector_store import VectorStore
            from vector_store import vector_store as new_store
            new_store.collection = new_store.client.get_or_create_collection(
                name="micronutrients",
                metadata={"hnsw:space": "cosine"}
            )
            new_store.is_initialized = False
            
            print("[OK] Ready for fresh initialization")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to delete collection: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Manage VitaCheck RAG Knowledge Base"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List command
    subparsers.add_parser('list', help='List all items in KB')
    
    # Stats command
    subparsers.add_parser('stats', help='Show KB statistics')
    
    # Delete item command
    delete_item_parser = subparsers.add_parser('delete-item', help='Delete specific item')
    delete_item_parser.add_argument('item_id', help='Item ID to delete')
    
    # Delete category command
    delete_cat_parser = subparsers.add_parser('delete-category', help='Delete all items in category')
    delete_cat_parser.add_argument('category', help='Category name (e.g., Vitamin, Mineral)')
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all data from KB')
    clear_parser.add_argument('--confirm', action='store_true', help='Skip confirmation')
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset to default micronutrients')
    reset_parser.add_argument('--confirm', action='store_true', help='Skip confirmation')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export KB to JSON')
    export_parser.add_argument('filepath', help='Path to export file')
    
    # Delete collection command
    delete_coll_parser = subparsers.add_parser('delete-collection', help='Delete entire ChromaDB collection')
    delete_coll_parser.add_argument('--confirm', action='store_true', help='Skip confirmation')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = KBManager()
    
    print("\n" + "="*70)
    print("VITACHECK RAG KB MANAGER")
    print("="*70)
    
    # Execute command
    if args.command == 'list':
        manager.list_items()
    elif args.command == 'stats':
        manager.get_stats()
    elif args.command == 'delete-item':
        manager.delete_item(args.item_id)
    elif args.command == 'delete-category':
        manager.delete_category(args.category)
    elif args.command == 'clear':
        manager.clear_all(args.confirm)
    elif args.command == 'reset':
        manager.reset_to_default(args.confirm)
    elif args.command == 'export':
        manager.export(args.filepath)
    elif args.command == 'delete-collection':
        manager.delete_collection(args.confirm)
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
