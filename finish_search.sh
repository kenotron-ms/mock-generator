#!/bin/bash
# Process remaining batches 7-10

cd /Users/ken/workspace/mock-generator
source .venv/bin/activate

echo "Processing remaining batches (7-10)..."
echo ""

for i in {1..4}; do
    echo "Running batch processor (attempt $i)..."
    python run_font_search.py 2>&1 | grep -E "(BATCH|Winners|COMPLETE)"
    echo ""
    sleep 2
done

echo "Checking final progress..."
python3 -c "import json; p=json.load(open('output/font-search-progress.json')); print(f'Complete: {len(p[\"completed_batches\"])}/10'); print('Semifinalists:'); [print(f'  - {f}') for f in sorted(set(p['semifinalists']))]"
