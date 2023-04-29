import os
import pytest
import zipfile
from archiver import Archiver


@pytest.fixture
def test_folder(tmp_path):
    # Create a temporary folder for testing
    test_dir = tmp_path / 'test_dir'
    test_dir.mkdir()
    # Create some test files
    with open(test_dir / 'file1.txt', 'w') as f:
        f.write('Test file 1')
    with open(test_dir / 'file2.csv', 'w') as f:
        f.write('Test file 2')
    with open(test_dir / 'temp_file.txt', 'w') as f:
        f.write('Temp file')
    yield test_dir
    # Clean up the temporary folder after the test completes
    for root, dirs, files in os.walk(test_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(test_dir)


def test_locate_files_include(test_folder):
    # Test that files matching include pattern are returned
    archiver = Archiver()
    files = archiver.locate_files(test_folder, '*.txt')
    assert len(files) == 2
    assert str(test_folder / 'file1.txt') in files
    assert str(test_folder / 'temp_file.txt') in files


def test_locate_files_no_include(test_folder):
    # Passing no include pattern should return all files
    archiver = Archiver()
    files = archiver.locate_files(test_folder)
    assert len(files) == 3


def test_locate_files_exclude(test_folder):
    # Test that files matching exclude pattern are not returned
    archiver = Archiver()
    files = archiver.locate_files(test_folder, '*', exclude_pattern='*temp*')
    assert len(files) == 2
    assert str(test_folder / 'file1.txt') in files
    assert str(test_folder / 'file2.csv') in files


@pytest.fixture
def test_files(tmp_path):
    # Create some test files
    file1_path = tmp_path / 'file1.txt'
    with open(file1_path, 'w') as f:
        f.write('Test file 1')
    file2_path = tmp_path / 'file2.csv'
    with open(file2_path, 'w') as f:
        f.write('Test file 2')
    yield [file1_path, file2_path]
    # Clean up the test files after the test completes
    for file_path in [file1_path, file2_path]:
        delete_test_file(file_path)


def delete_test_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def test_zip_files(test_files, tmp_path):
    # Test that zip file is created with correct contents
    archiver = Archiver()
    zip_path = tmp_path / 'test.zip'
    archiver.zip_files(test_files, zip_path)
    with zipfile.ZipFile(zip_path) as zip_file:
        assert len(zip_file.namelist()) == 2
        assert 'file1.txt' in zip_file.namelist()
        assert 'file2.csv' in zip_file.namelist()
        with zip_file.open('file1.txt') as f:
            assert f.read().decode('utf-8') == 'Test file 1'
        with zip_file.open('file2.csv') as f:
            assert f.read().decode('utf-8') == 'Test file 2'


def test_archive(test_files, tmp_path):
    # Test the archive function
    archiver = Archiver()
    zip_path = tmp_path / 'test.zip'
    archiver.archive(tmp_path, str(zip_path), "", "*.csv")

    with zipfile.ZipFile(zip_path) as zip_file:
        assert len(zip_file.namelist()) == 1
        assert 'file1.txt' in zip_file.namelist()
