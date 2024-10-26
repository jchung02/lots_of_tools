import pandas as pd

def load_and_split_data(train_path, test_path, output_train_path, output_test_path, train_size=0.8, random_state=42):
    # Load the saved train and test CSV files
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    # Merge the train and test DataFrames
    full_df = pd.concat([train_df, test_df], ignore_index=True)

    # Shuffle the full dataset
    full_df = full_df.sample(frac=1, random_state=random_state).reset_index(drop=True)

    # Perform new train-test split (80% train, 20% test)
    train_df = full_df.sample(frac=train_size, random_state=random_state)
    test_df = full_df.drop(train_df.index)

    # Save the new train and test datasets to CSV
    train_df.to_csv(output_train_path, index=False)
    test_df.to_csv(output_test_path, index=False)

    print(f"New Train data size: {len(train_df)}")
    print(f"New Test data size: {len(test_df)}")
    
