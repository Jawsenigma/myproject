echo "BUILD START"

python3.12 -m pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput 

mv staticfiles_build/static /vercel/path0/staticfiles_build/static

echo "BUILD END" 